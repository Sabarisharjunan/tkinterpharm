"""Record repository for record data access."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.record import Record, RecordStatusEnum
from app.repositories.base_repository import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository for Record model."""

    def __init__(self, session: Session):
        """Initialize record repository."""
        super().__init__(Record, session)

    def get_by_status(self, status: RecordStatusEnum, skip: int = 0, limit: int = 100) -> List[Record]:
        """Get records by status.

        Args:
            status: Record status
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of records with specified status
        """
        return (
            self.session.query(Record)
            .filter(Record.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Record]:
        """Get records by category.

        Args:
            category: Record category
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of records in category
        """
        return (
            self.session.query(Record)
            .filter(Record.category == category)
            .filter(Record.deleted_at == None)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_records(self, skip: int = 0, limit: int = 100) -> List[Record]:
        """Get active records (not deleted).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active records
        """
        return (
            self.session.query(Record)
            .filter(Record.deleted_at == None)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def soft_delete(self, record_id: int) -> bool:
        """Soft delete a record.

        Args:
            record_id: Record ID

        Returns:
            True if deleted, False otherwise
        """
        record = self.get_by_id(record_id)
        if record:
            record.deleted_at = datetime.utcnow()
            self.session.commit()
            return True
        return False

    def search_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[Record]:
        """Search records by title.

        Args:
            title: Title to search for
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching records
        """
        return (
            self.session.query(Record)
            .filter(Record.title.ilike(f"%{title}%"))
            .filter(Record.deleted_at == None)
            .offset(skip)
            .limit(limit)
            .all()
        )
