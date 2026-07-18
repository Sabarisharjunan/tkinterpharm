"""Notification service for managing notifications."""

from typing import List
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationTypeEnum
from app.repositories.notification_repository import NotificationRepository
from app.utils.logger import get_logger
from app.exceptions import NotFoundException

logger = get_logger(__name__)


class NotificationService:
    """Notification management service."""

    def __init__(self, session: Session):
        """Initialize notification service.

        Args:
            session: Database session
        """
        self.notification_repo = NotificationRepository(session)
        self.session = session

    def create_notification(
        self,
        user_id: int,
        message: str,
        title: str = None,
        notification_type: str = "INFO",
    ) -> Notification:
        """Create a notification.

        Args:
            user_id: User ID
            message: Notification message
            title: Notification title
            notification_type: Notification type (INFO, SUCCESS, WARNING, ERROR)

        Returns:
            Created notification
        """
        try:
            notif_type = NotificationTypeEnum[notification_type.upper()]
        except KeyError:
            notif_type = NotificationTypeEnum.INFO

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notif_type,
        )

        notification = self.notification_repo.create(notification)
        logger.info(f"Notification created for user {user_id}")
        return notification

    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Notification]:
        """Get user notifications.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of notifications
        """
        return self.notification_repo.get_user_notifications(user_id, skip, limit)

    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications.

        Args:
            user_id: User ID

        Returns:
            Number of unread notifications
        """
        return self.notification_repo.get_unread_count(user_id)

    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read.

        Args:
            notification_id: Notification ID

        Returns:
            True if marked
        """
        return self.notification_repo.mark_as_read(notification_id)

    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user notifications as read.

        Args:
            user_id: User ID

        Returns:
            Number of notifications marked
        """
        return self.notification_repo.mark_all_as_read(user_id)

    def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification.

        Args:
            notification_id: Notification ID

        Returns:
            True if deleted
        """
        return self.notification_repo.delete(notification_id)
