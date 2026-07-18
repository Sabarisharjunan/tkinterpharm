"""Settings model."""

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Index, Text

from app.models.base_model import BaseModel


class Settings(BaseModel):
    """Settings model for application and user preferences."""

    __tablename__ = "settings"

    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    data_type = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
    is_global = Column(Boolean, default=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    __table_args__ = (
        Index("idx_settings_key", "key"),
        Index("idx_settings_user", "user_id"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Settings(key={self.key}, value={self.value})>"
