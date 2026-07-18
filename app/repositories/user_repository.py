"""User repository for user data access."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    def __init__(self, session: Session):
        """Initialize user repository."""
        super().__init__(User, session)

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username to search for

        Returns:
            User instance or None
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: Email to search for

        Returns:
            User instance or None
        """
        return self.session.query(User).filter(User.email == email).first()

    def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        return (
            self.session.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_role(self, role: str, skip: int = 0, limit: int = 100):
        """Get users by role.

        Args:
            role: User role
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users with specified role
        """
        return (
            self.session.query(User)
            .filter(User.role == role)
            .offset(skip)
            .limit(limit)
            .all()
        )
