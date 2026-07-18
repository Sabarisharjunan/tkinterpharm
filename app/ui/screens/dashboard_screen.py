"""Dashboard screen."""

import tkinter as tk
from typing import Optional
from datetime import datetime

from app.ui.widgets.frame import ThemedFrame
from app.ui.widgets.label import ThemedLabel
from app.ui.widgets.button import ThemedButton
from app.ui.notifications import show_toast
from app.state.user_context import UserContext
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DashboardScreen(ThemedFrame):
    """Dashboard screen."""

    def __init__(
        self,
        parent: tk.Widget = None,
        user_context: UserContext = None,
        **kwargs
    ):
        """Initialize dashboard screen.

        Args:
            parent: Parent widget
            user_context: Current user context
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        self.user_context = user_context
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create dashboard widgets."""
        # Header
        header_frame = ThemedFrame(self)
        header_frame.pack(fill="x", padx=16, pady=16)

        title = ThemedLabel(
            header_frame,
            text="Dashboard",
            style="header",
        )
        title.pack(anchor="w")

        # Welcome message
        welcome_text = f"Welcome, {self.user_context.full_name}!"
        welcome_label = ThemedLabel(
            header_frame,
            text=welcome_text,
        )
        welcome_label.pack(anchor="w", pady=(4, 0))

        # Stats cards
        stats_frame = ThemedFrame(self)
        stats_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Example stat card
        stat_card = self._create_stat_card(
            stats_frame,
            title="Total Records",
            value="0",
            color=self.get_color("primary"),
        )
        stat_card.pack(fill="x", pady=(0, 10))

        stat_card2 = self._create_stat_card(
            stats_frame,
            title="Active Users",
            value="0",
            color=self.get_color("success"),
        )
        stat_card2.pack(fill="x", pady=(0, 10))

        # Info
        info_label = ThemedLabel(
            stats_frame,
            text=f"Last login: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            style="small",
        )
        info_label.pack(anchor="w", pady=(20, 0))

    def _create_stat_card(
        self,
        parent: tk.Widget,
        title: str,
        value: str,
        color: str,
    ) -> tk.Frame:
        """Create a stat card.

        Args:
            parent: Parent widget
            title: Card title
            value: Card value
            color: Card color

        Returns:
            Stat card frame
        """
        card = tk.Frame(
            parent,
            bg=color,
            padx=16,
            pady=16,
            relief=tk.FLAT,
        )

        value_label = tk.Label(
            card,
            text=value,
            bg=color,
            fg="#FFFFFF",
            font=("Arial", 24, "bold"),
        )
        value_label.pack(anchor="w")

        title_label = tk.Label(
            card,
            text=title,
            bg=color,
            fg="#FFFFFF",
            font=("Arial", 10),
        )
        title_label.pack(anchor="w")

        return card

    def on_enter(self) -> None:
        """Called when screen is shown."""
        logger.debug("Dashboard screen entered")

    def refresh(self) -> None:
        """Refresh dashboard data."""
        logger.debug("Dashboard refreshed")
