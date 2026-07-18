"""Application-wide constants and enumerations."""

from enum import Enum


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"


class RecordStatus(Enum):
    """Record status enumeration."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class NotificationType(Enum):
    """Notification type enumeration."""
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class AppConstants:
    """Application constants."""
    APP_NAME = "TkinTermPharm"
    APP_VERSION = "1.0.0"
    DEFAULT_PAGINATION_SIZE = 25
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 50
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
