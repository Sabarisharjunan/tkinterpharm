"""User service for user management."""

from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User, UserRoleEnum
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditRepository
from app.utils.logger import get_logger
from app.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException,
    AuthorizationException,
)
from app.utils.security import SecurityUtils

logger = get_logger(__name__)


class UserService:
    """User management service."""

    def __init__(self, session: Session):
        """Initialize user service.

        Args:
            session: Database session
        """
        self.user_repo = UserRepository(session)
        self.audit_repo = AuditRepository(session)
        self.session = session

    def get_user(self, user_id: int) -> User:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User instance

        Raises:
            NotFoundException: If user not found
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users
        """
        return self.user_repo.get_all(skip, limit)

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        return self.user_repo.get_active_users(skip, limit)

    def update_user(
        self,
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        role: str = None,
        is_active: bool = None,
        updated_by: int = None,
    ) -> User:
        """Update user.

        Args:
            user_id: User ID
            first_name: New first name
            last_name: New last name
            email: New email
            role: New role
            is_active: Active status
            updated_by: ID of user making the change

        Returns:
            Updated user
        """
        user = self.get_user(user_id)
        updates = {}

        if first_name is not None:
            updates["first_name"] = first_name
        if last_name is not None:
            updates["last_name"] = last_name
        if email is not None:
            # Check if email is already in use
            existing = self.user_repo.get_by_email(email)
            if existing and existing.id != user_id:
                raise ConflictException(f"Email '{email}' already in use")
            updates["email"] = email
        if role is not None:
            try:
                updates["role"] = UserRoleEnum[role.upper()]
            except KeyError:
                raise ValidationException(f"Invalid role: {role}")
        if is_active is not None:
            updates["is_active"] = is_active

        updated_user = self.user_repo.update(user_id, updates)
        logger.info(f"User updated: {user.username}")
        return updated_user

    def deactivate_user(self, user_id: int) -> User:
        """Deactivate user.

        Args:
            user_id: User ID

        Returns:
            Deactivated user
        """
        return self.update_user(user_id, is_active=False)

    def activate_user(self, user_id: int) -> User:
        """Activate user.

        Args:
            user_id: User ID

        Returns:
            Activated user
        """
        return self.update_user(user_id, is_active=True)

    def count_users(self) -> int:
        """Count total users.

        Returns:
            Number of users
        """
        return self.user_repo.count()

    def count_active_users(self) -> int:
        """Count active users.

        Returns:
            Number of active users
        """
        return self.session.query(User).filter(User.is_active == True).count()
