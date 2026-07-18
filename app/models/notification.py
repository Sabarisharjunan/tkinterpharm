"""Notification model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum, Index
import enum

from app.models.base_model import BaseModel


class NotificationTypeEnum(str, enum.Enum):
    """Notification type enumeration."""
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Notification(BaseModel):
    """Notification model."""

    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    message = Column(String(1000), nullable=False)
    type = Column(Enum(NotificationTypeEnum), default=NotificationTypeEnum.INFO, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_notification_user", "user_id"),
        Index("idx_notification_read", "is_read"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Notification(user_id={self.user_id}, type={self.type})>"
