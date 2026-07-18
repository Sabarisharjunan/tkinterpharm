"""Main application window."""

import tkinter as tk
from typing import Optional, Dict, Callable
from datetime import datetime

from app.ui.widgets.frame import ThemedFrame
from app.ui.widgets.label import ThemedLabel
from app.ui.widgets.button import ThemedButton
from app.ui.screens.login_screen import LoginScreen
from app.ui.screens.dashboard_screen import DashboardScreen
from app.ui.screens.user_screen import UserManagementScreen
from app.ui.theme_manager import get_theme_manager
from app.di import get_container
from app.state import get_app_state, UserContext
from app.config import get_config
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(tk.Tk):
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.config = get_config()
        self.theme_manager = get_theme_manager(self.config.get("app.theme", "light"))
        self.container = get_container()
        self.app_state = get_app_state()

        # Configure window
        self.title(f"{self.config.get('app.name')} v{self.config.get('app.version')}")
        self.geometry(
            f"{self.config.get('ui.window_width')}x{self.config.get('ui.window_height')}"
        )
        self.minsize(800, 600)

        # Initialize screens
        self.screens: Dict[str, tk.Widget] = {}
        self.current_screen: Optional[str] = None
        self._create_screens()

        # Show login screen
        self._show_screen("login")

        logger.info("Main window initialized")

    def _create_screens(self) -> None:
        """Create all screens."""
        # Create container for screens
        self.screen_container = ThemedFrame(self)
        self.screen_container.pack(fill="both", expand=True)

        # Login screen
        auth_service = self.container.get("auth_service")
        login_screen = LoginScreen(
            self.screen_container,
            auth_service=auth_service,
            on_login_success=self._on_login_success,
        )
        self.screens["login"] = login_screen

        # Dashboard screen
        dashboard_screen = DashboardScreen(
            self.screen_container,
            user_context=self.app_state.user_context,
        )
        self.screens["dashboard"] = dashboard_screen

        # User management screen
        user_service = self.container.get("user_service")
        user_screen = UserManagementScreen(
            self.screen_container,
            user_service=user_service,
        )
        self.screens["users"] = user_screen

    def _show_screen(self, screen_name: str) -> None:
        """Show a screen.

        Args:
            screen_name: Screen name
        """
        if screen_name not in self.screens:
            logger.warning(f"Screen not found: {screen_name}")
            return

        # Hide current screen
        if self.current_screen and self.current_screen in self.screens:
            self.screens[self.current_screen].pack_forget()
            if hasattr(self.screens[self.current_screen], "on_exit"):
                self.screens[self.current_screen].on_exit()

        # Show new screen
        self.screens[screen_name].pack(fill="both", expand=True)
        if hasattr(self.screens[screen_name], "on_enter"):
            self.screens[screen_name].on_enter()

        self.current_screen = screen_name
        self.app_state.set_current_screen(screen_name)
        logger.debug(f"Showing screen: {screen_name}")

    def _on_login_success(self, user_context: UserContext) -> None:
        """Handle successful login.

        Args:
            user_context: User context
        """
        self.app_state.set_current_user(user_context)
        self._show_screen("dashboard")

    def show_dashboard(self) -> None:
        """Show dashboard screen."""
        self._show_screen("dashboard")

    def show_users(self) -> None:
        """Show user management screen."""
        self._show_screen("users")

    def logout(self) -> None:
        """Logout current user."""
        self.app_state.clear_current_user()
        self._show_screen("login")
        logger.info("User logged out")

    def run(self) -> None:
        """Run the application."""
        self.app_state.is_running = True
        logger.info("Application started")
        self.mainloop()

    def on_closing(self) -> None:
        """Handle window closing."""
        logger.info("Application closing")
        self.app_state.is_running = False
        self.destroy()


def create_app() -> MainWindow:
    """Create and return main application window.

    Returns:
        MainWindow instance
    """
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    return app
