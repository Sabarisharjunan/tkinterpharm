"""Audit log repository for audit data access."""

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    """Repository for AuditLog model."""

    def __init__(self, session: Session):
        """Initialize audit repository."""
        super().__init__(AuditLog, session)

    def get_by_entity(self, entity_type: str, entity_id: int) -> List[AuditLog]:
        """Get audit logs for an entity.

        Args:
            entity_type: Entity type
            entity_id: Entity ID

        Returns:
            List of audit logs for entity
        """
        return (
            self.session.query(AuditLog)
            .filter(AuditLog.entity_type == entity_type)
            .filter(AuditLog.entity_id == entity_id)
            .order_by(AuditLog.created_at.desc())
            .all()
        )

    def get_by_action(self, action: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by action.

        Args:
            action: Action type (CREATE, UPDATE, DELETE, LOGIN)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        return (
            self.session.query(AuditLog)
            .filter(AuditLog.action == action)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by user.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        return (
            self.session.query(AuditLog)
            .filter(AuditLog.changed_by == user_id)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent(self, hours: int = 24, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs.

        Args:
            hours: Number of hours to look back
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of recent audit logs
        """
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.session.query(AuditLog)
            .filter(AuditLog.created_at >= since)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
