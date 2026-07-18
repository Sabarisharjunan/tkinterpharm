"""Dependency Injection Container."""

from typing import Dict, Any, Callable, Optional
from sqlalchemy.orm import Session

from app.database import create_session
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.record_service import RecordService
from app.services.notification_service import NotificationService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DIContainer:
    """Dependency injection container."""

    def __init__(self):
        """Initialize DI container."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}

    def register_singleton(self, name: str, instance: Any) -> None:
        """Register a singleton service.

        Args:
            name: Service name
            instance: Service instance
        """
        self._singletons[name] = instance
        logger.debug(f"Registered singleton: {name}")

    def register_factory(self, name: str, factory: Callable) -> None:
        """Register a factory function.

        Args:
            name: Service name
            factory: Factory function that creates the service
        """
        self._factories[name] = factory
        logger.debug(f"Registered factory: {name}")

    def get(self, name: str) -> Any:
        """Get a service.

        Args:
            name: Service name

        Returns:
            Service instance

        Raises:
            KeyError: If service not found
        """
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]

        # Check factories
        if name in self._factories:
            return self._factories[name]()

        raise KeyError(f"Service not found: {name}")

    def has(self, name: str) -> bool:
        """Check if service exists.

        Args:
            name: Service name

        Returns:
            True if service exists
        """
        return name in self._singletons or name in self._factories


# Global container instance
_container: Optional[DIContainer] = None


def get_container() -> DIContainer:
    """Get global DI container.

    Returns:
        DIContainer instance
    """
    global _container
    if _container is None:
        _container = DIContainer()
        _setup_services(_container)
    return _container


def _setup_services(container: DIContainer) -> None:
    """Set up all services in the container.

    Args:
        container: DI container
    """
    # Register session factory
    def session_factory() -> Session:
        return create_session()

    container.register_factory("session", session_factory)

    # Register services
    def auth_service_factory() -> AuthService:
        session = container.get("session")
        return AuthService(session)

    def user_service_factory() -> UserService:
        session = container.get("session")
        return UserService(session)

    def record_service_factory() -> RecordService:
        session = container.get("session")
        return RecordService(session)

    def notification_service_factory() -> NotificationService:
        session = container.get("session")
        return NotificationService(session)

    container.register_factory("auth_service", auth_service_factory)
    container.register_factory("user_service", user_service_factory)
    container.register_factory("record_service", record_service_factory)
    container.register_factory("notification_service", notification_service_factory)

    logger.info("DI container initialized with all services")
