"""Notification repository for notification data access."""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.notification import Notification, NotificationTypeEnum
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification model."""

    def __init__(self, session: Session):
        """Initialize notification repository."""
        super().__init__(Notification, session)

    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Notification]:
        """Get user notifications.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of user notifications
        """
        return (
            self.session.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for user.

        Args:
            user_id: User ID

        Returns:
            Number of unread notifications
        """
        return (
            self.session.query(Notification)
            .filter(Notification.user_id == user_id)
            .filter(Notification.is_read == False)
            .count()
        )

    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read.

        Args:
            notification_id: Notification ID

        Returns:
            True if marked, False otherwise
        """
        notification = self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.session.commit()
            return True
        return False

    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user notifications as read.

        Args:
            user_id: User ID

        Returns:
            Number of notifications marked
        """
        count = (
            self.session.query(Notification)
            .filter(Notification.user_id == user_id)
            .filter(Notification.is_read == False)
            .update({Notification.is_read: True, Notification.read_at: datetime.utcnow()})
        )
        self.session.commit()
        return count
