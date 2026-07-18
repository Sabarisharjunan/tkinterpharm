"""User model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Boolean, DateTime, Index, Enum
import enum

from app.models.base_model import BaseModel


class UserRoleEnum(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_users_username", "username"),
        Index("idx_users_email", "email"),
        Index("idx_users_role", "role"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(username={self.username}, email={self.email})>"

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        if not self.locked_until:
            return False
        return datetime.utcnow() < self.locked_until
