"""Generic Record model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey, Enum, Index, Text
import enum

from app.models.base_model import BaseModel


class RecordStatusEnum(str, enum.Enum):
    """Record status enumeration."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class Record(BaseModel):
    """Generic record model for storing various data."""

    __tablename__ = "records"

    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(RecordStatusEnum), default=RecordStatusEnum.DRAFT, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    data = Column(JSON, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_record_title", "title"),
        Index("idx_record_status", "status"),
        Index("idx_record_category", "category"),
        Index("idx_record_created_by", "created_by"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Record(title={self.title}, status={self.status})>"
