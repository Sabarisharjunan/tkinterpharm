"""Authentication service."""

from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.models.user import User, UserRoleEnum
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditRepository
from app.utils.logger import get_logger
from app.utils.security import SecurityUtils
from app.exceptions import (
    AuthenticationException,
    NotFoundException,
    ConflictException,
    ValidationException,
)
from app.config import get_config

logger = get_logger(__name__)


class AuthService:
    """Authentication service."""

    def __init__(self, session: Session):
        """Initialize authentication service.

        Args:
            session: Database session
        """
        self.user_repo = UserRepository(session)
        self.audit_repo = AuditRepository(session)
        self.session = session
        self.config = get_config()

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str = "USER",
    ) -> User:
        """Register a new user.

        Args:
            username: Username
            email: Email address
            password: Password
            first_name: First name
            last_name: Last name
            role: User role

        Returns:
            Created user

        Raises:
            ValidationException: If validation fails
            ConflictException: If user already exists
        """
        # Check if user exists
        if self.user_repo.get_by_username(username):
            raise ConflictException(f"Username '{username}' already exists")

        if self.user_repo.get_by_email(email):
            raise ConflictException(f"Email '{email}' already registered")

        # Validate password strength
        is_strong, msg = SecurityUtils.validate_password_strength(password)
        if not is_strong:
            raise ValidationException(msg)

        # Hash password
        password_hash = SecurityUtils.hash_password(password)

        # Create user
        try:
            role_enum = UserRoleEnum[role.upper()]
        except KeyError:
            raise ValidationException(f"Invalid role: {role}")

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role_enum,
            is_active=True,
        )

        user = self.user_repo.create(user)
        logger.info(f"User registered: {username}")
        return user

    def authenticate(
        self,
        username: str,
        password: str,
        ip_address: str = None,
    ) -> Tuple[User, bool]:
        """Authenticate user.

        Args:
            username: Username
            password: Password
            ip_address: IP address for logging

        Returns:
            Tuple of (user, success)

        Raises:
            AuthenticationException: If authentication fails
        """
        user = self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"Login attempt for non-existent user: {username}")
            raise AuthenticationException("Invalid username or password")

        # Check if user is active
        if not user.is_active:
            raise AuthenticationException("User account is inactive")

        # Check if user is locked
        if user.is_locked:
            raise AuthenticationException("User account is locked. Please try again later.")

        # Verify password
        if not SecurityUtils.verify_password(password, user.password_hash):
            user.failed_login_attempts += 1

            # Lock account if too many failed attempts
            if user.failed_login_attempts >= self.config.get("security.max_login_attempts"):
                lockout_minutes = self.config.get("security.lockout_minutes")
                user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
                logger.warning(f"User account locked: {username}")

            self.session.commit()
            raise AuthenticationException("Invalid username or password")

        # Reset failed attempts and update last login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        self.session.commit()

        logger.info(f"User authenticated: {username}")
        return user, True

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password.

        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password

        Returns:
            True if changed successfully

        Raises:
            AuthenticationException: If old password is incorrect
            ValidationException: If new password is invalid
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User")

        # Verify old password
        if not SecurityUtils.verify_password(old_password, user.password_hash):
            raise AuthenticationException("Invalid current password")

        # Validate new password
        is_strong, msg = SecurityUtils.validate_password_strength(new_password)
        if not is_strong:
            raise ValidationException(msg)

        # Update password
        user.password_hash = SecurityUtils.hash_password(new_password)
        self.session.commit()

        logger.info(f"Password changed for user: {user.username}")
        return True

    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reset user password (admin function).

        Args:
            user_id: User ID
            new_password: New password

        Returns:
            True if reset successfully
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User")

        user.password_hash = SecurityUtils.hash_password(new_password)
        self.session.commit()

        logger.info(f"Password reset for user: {user.username}")
        return True

    def unlock_user(self, user_id: int) -> bool:
        """Unlock a locked user account.

        Args:
            user_id: User ID

        Returns:
            True if unlocked
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User")

        user.locked_until = None
        user.failed_login_attempts = 0
        self.session.commit()

        logger.info(f"User unlocked: {user.username}")
        return True
