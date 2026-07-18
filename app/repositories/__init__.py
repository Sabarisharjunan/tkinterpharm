"""Repository pattern implementation for data access."""

from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: type[T], session: Session):
        """Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Database session
        """
        self.model = model
        self.session = session

    def create(self, obj: T) -> T:
        """Create a new record.

        Args:
            obj: Model instance to create

        Returns:
            Created model instance
        """
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, obj_id: int) -> Optional[T]:
        """Get record by ID.

        Args:
            obj_id: Record ID

        Returns:
            Model instance or None
        """
        return self.session.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, obj_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update a record.

        Args:
            obj_id: Record ID
            data: Dictionary of fields to update

        Returns:
            Updated model instance or None
        """
        obj = self.get_by_id(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.session.commit()
            self.session.refresh(obj)
        return obj

    def delete(self, obj_id: int) -> bool:
        """Delete a record.

        Args:
            obj_id: Record ID

        Returns:
            True if deleted, False otherwise
        """
        obj = self.get_by_id(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False

    def count(self) -> int:
        """Count total records.

        Returns:
            Total number of records
        """
        return self.session.query(self.model).count()

    def exists(self, obj_id: int) -> bool:
        """Check if record exists.

        Args:
            obj_id: Record ID

        Returns:
            True if exists, False otherwise
        """
        return self.session.query(self.model).filter(self.model.id == obj_id).first() is not None
