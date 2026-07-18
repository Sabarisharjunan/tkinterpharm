"""Global application state."""

from typing import Optional, Dict, Any, Callable, List

from app.state.user_context import UserContext
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AppState:
    """Central application state manager."""

    def __init__(self):
        """Initialize application state."""
        self.user_context = UserContext()
        self.current_screen: Optional[str] = None
        self.is_running = False
        self.data: Dict[str, Any] = {}
        self._observers: Dict[str, List[Callable]] = {}

    def set_current_user(self, user_context: UserContext) -> None:
        """Set current user context."""
        self.user_context = user_context
        self._notify_observers("user_changed")
        logger.info(f"User set: {user_context.username}")

    def clear_current_user(self) -> None:
        """Clear current user context."""
        self.user_context.clear()
        self._notify_observers("user_changed")
        logger.info("User cleared")

    def set_current_screen(self, screen_name: str) -> None:
        """Set current screen."""
        self.current_screen = screen_name
        self._notify_observers("screen_changed")

    def set_data(self, key: str, value: Any) -> None:
        """Set application data."""
        self.data[key] = value
        self._notify_observers(f"data_changed:{key}")

    def get_data(self, key: str, default: Any = None) -> Any:
        """Get application data."""
        return self.data.get(key, default)

    def subscribe(self, event: str, callback: Callable) -> None:
        """Subscribe to state changes."""
        if event not in self._observers:
            self._observers[event] = []
        self._observers[event].append(callback)

    def _notify_observers(self, event: str) -> None:
        """Notify observers of state change."""
        if event in self._observers:
            for callback in self._observers[event]:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error notifying observer: {str(e)}")


_app_state: Optional[AppState] = None


def get_app_state() -> AppState:
    """Get global application state."""
    global _app_state
    if _app_state is None:
        _app_state = AppState()
    return _app_state
