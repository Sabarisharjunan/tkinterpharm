"""Application-level exception classes."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        """Initialize exception."""
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation."""
        return f"[{self.code}] {self.message}"


class ValidationException(AppException):
    """Raised when data validation fails."""

    def __init__(self, message: str, field: str = None):
        """Initialize exception."""
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class AuthenticationException(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        """Initialize exception."""
        super().__init__(message, "AUTH_FAILED")


class AuthorizationException(AppException):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Access denied"):
        """Initialize exception."""
        super().__init__(message, "AUTH_DENIED")


class NotFoundException(AppException):
    """Raised when resource is not found."""

    def __init__(self, resource: str, identifier: str = None):
        """Initialize exception."""
        msg = f"{resource} not found"
        if identifier:
            msg += f" (ID: {identifier})"
        super().__init__(msg, "NOT_FOUND")


class ConflictException(AppException):
    """Raised when resource conflicts (e.g., duplicate)."""

    def __init__(self, message: str):
        """Initialize exception."""
        super().__init__(message, "CONFLICT")
