"""Audit log model."""

from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey, Index

from app.models.base_model import BaseModel


class AuditLog(BaseModel):
    """Audit log model for tracking changes."""

    __tablename__ = "audit_logs"

    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    action = Column(String(50), nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    __table_args__ = (
        Index("idx_audit_entity", "entity_type", "entity_id"),
        Index("idx_audit_action", "action"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<AuditLog({self.entity_type}:{self.entity_id} {self.action})>"
