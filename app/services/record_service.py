"""Record service for record management."""

from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.record import Record, RecordStatusEnum
from app.repositories.record_repository import RecordRepository
from app.repositories.audit_repository import AuditRepository
from app.utils.logger import get_logger
from app.exceptions import NotFoundException, ValidationException

logger = get_logger(__name__)


class RecordService:
    """Record management service."""

    def __init__(self, session: Session):
        """Initialize record service.

        Args:
            session: Database session
        """
        self.record_repo = RecordRepository(session)
        self.audit_repo = AuditRepository(session)
        self.session = session

    def create_record(
        self,
        title: str,
        description: str = None,
        category: str = None,
        data: Dict[str, Any] = None,
        created_by: int = None,
    ) -> Record:
        """Create a new record.

        Args:
            title: Record title
            description: Record description
            category: Record category
            data: Additional data as JSON
            created_by: User ID of creator

        Returns:
            Created record
        """
        if not title or len(title) < 3:
            raise ValidationException("Title must be at least 3 characters")

        record = Record(
            title=title,
            description=description,
            category=category,
            data=data or {},
            created_by=created_by,
            status=RecordStatusEnum.DRAFT,
        )

        record = self.record_repo.create(record)
        logger.info(f"Record created: {record.title}")
        return record

    def get_record(self, record_id: int) -> Record:
        """Get record by ID.

        Args:
            record_id: Record ID

        Returns:
            Record instance

        Raises:
            NotFoundException: If record not found
        """
        record = self.record_repo.get_by_id(record_id)
        if not record:
            raise NotFoundException("Record", str(record_id))
        return record

    def get_all_records(self, skip: int = 0, limit: int = 100) -> List[Record]:
        """Get all active records.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of records
        """
        return self.record_repo.get_active_records(skip, limit)

    def get_records_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Record]:
        """Get records by category.

        Args:
            category: Category name
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of records
        """
        return self.record_repo.get_by_category(category, skip, limit)

    def search_records(self, query: str, skip: int = 0, limit: int = 100) -> List[Record]:
        """Search records by title.

        Args:
            query: Search query
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching records
        """
        return self.record_repo.search_by_title(query, skip, limit)

    def update_record(
        self,
        record_id: int,
        title: str = None,
        description: str = None,
        category: str = None,
        status: str = None,
        data: Dict[str, Any] = None,
        updated_by: int = None,
    ) -> Record:
        """Update record.

        Args:
            record_id: Record ID
            title: New title
            description: New description
            category: New category
            status: New status
            data: Additional data
            updated_by: User ID of updater

        Returns:
            Updated record
        """
        record = self.get_record(record_id)
        updates = {}

        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if category is not None:
            updates["category"] = category
        if status is not None:
            try:
                updates["status"] = RecordStatusEnum[status.upper()]
            except KeyError:
                raise ValidationException(f"Invalid status: {status}")
        if data is not None:
            updates["data"] = data
        if updated_by is not None:
            updates["updated_by"] = updated_by

        updated_record = self.record_repo.update(record_id, updates)
        logger.info(f"Record updated: {record.title}")
        return updated_record

    def delete_record(self, record_id: int) -> bool:
        """Soft delete record.

        Args:
            record_id: Record ID

        Returns:
            True if deleted
        """
        record = self.get_record(record_id)
        result = self.record_repo.soft_delete(record_id)
        if result:
            logger.info(f"Record deleted: {record.title}")
        return result

    def count_records(self) -> int:
        """Count total active records.

        Returns:
            Number of records
        """
        return self.session.query(Record).filter(Record.deleted_at == None).count()
