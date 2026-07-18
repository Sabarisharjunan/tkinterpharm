"""User context for current session."""

from typing import Optional
from dataclasses import dataclass


@dataclass
class UserContext:
    """Current user context."""

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_authenticated: bool = False

    def clear(self) -> None:
        """Clear user context."""
        self.user_id = None
        self.username = None
        self.email = None
        self.full_name = None
        self.role = None
        self.is_authenticated = False

    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == "ADMIN"

    def is_manager(self) -> bool:
        """Check if user is manager."""
        return self.role in ["MANAGER", "ADMIN"]
