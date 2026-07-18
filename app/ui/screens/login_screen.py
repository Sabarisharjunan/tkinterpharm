"""Login screen."""

import tkinter as tk
from typing import Callable, Optional

from app.ui.widgets.frame import ThemedFrame
from app.ui.widgets.label import ThemedLabel
from app.ui.widgets.button import ThemedButton
from app.ui.widgets.entry import ThemedEntry
from app.ui.dialogs import show_error, show_info
from app.services.auth_service import AuthService
from app.state.user_context import UserContext
from app.exceptions import AuthenticationException, ValidationException
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LoginScreen(ThemedFrame):
    """Login screen."""

    def __init__(
        self,
        parent: tk.Widget = None,
        auth_service: AuthService = None,
        on_login_success: Callable = None,
        **kwargs
    ):
        """Initialize login screen.

        Args:
            parent: Parent widget
            auth_service: Authentication service
            on_login_success: Callback on successful login
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, padded=True, **kwargs)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create login screen widgets."""
        # Title
        title = ThemedLabel(
            self,
            text="TkinTermPharm",
            style="header",
        )
        title.pack(pady=(0, 20))

        subtitle = ThemedLabel(
            self,
            text="Pharmacy Management System",
        )
        subtitle.pack(pady=(0, 40))

        # Login form frame
        form_frame = ThemedFrame(self)
        form_frame.pack(fill="x", padx=40, pady=20)

        # Username
        self.username_entry = ThemedEntry(
            form_frame,
            label="Username",
            placeholder="Enter your username",
        )
        self.username_entry.pack(fill="x", pady=(0, 16))

        # Password
        self.password_entry = ThemedEntry(
            form_frame,
            label="Password",
            placeholder="Enter your password",
            show="•",
        )
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Remember me
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            form_frame,
            text="Remember me",
            variable=self.remember_var,
            bg=self.get_color("bg"),
            fg=self.get_color("fg"),
            selectcolor=self.get_color("primary"),
        )
        remember_check.pack(anchor="w", pady=(0, 20))

        # Login button
        login_btn = ThemedButton(
            form_frame,
            text="Login",
            command=self._on_login_click,
            button_type="primary",
        )
        login_btn.pack(fill="x", pady=(0, 10))

        # Status label
        self.status_label = ThemedLabel(
            form_frame,
            text="",
        )
        self.status_label.pack(pady=(20, 0))

    def _on_login_click(self) -> None:
        """Handle login button click."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            show_error(self, "Validation Error", "Please enter both username and password")
            return

        try:
            user, success = self.auth_service.authenticate(username, password)
            if success:
                # Create user context
                user_context = UserContext.from_user(user)
                logger.info(f"User logged in: {username}")
                if self.on_login_success:
                    self.on_login_success(user_context)
        except AuthenticationException as e:
            show_error(self, "Login Failed", str(e))
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            show_error(self, "Error", "An error occurred during login")

    def clear(self) -> None:
        """Clear login form."""
        self.username_entry.clear()
        self.password_entry.clear()
