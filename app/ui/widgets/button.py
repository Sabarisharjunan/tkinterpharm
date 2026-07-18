"""Custom themed button."""

import tkinter as tk
from typing import Optional, Callable

from app.ui.widgets.base_widget import ThemedWidget


class ThemedButton(tk.Button):
    """Custom themed button."""

    def __init__(
        self,
        parent: tk.Widget = None,
        text: str = "",
        command: Optional[Callable] = None,
        button_type: str = "primary",
        **kwargs
    ):
        """Initialize themed button.

        Args:
            parent: Parent widget
            text: Button text
            command: Button command
            button_type: Button type (primary, secondary, success, warning, error)
            **kwargs: Additional keyword arguments
        """
        from app.ui.theme_manager import get_theme_manager
        theme_manager = get_theme_manager()
        colors = theme_manager.get_colors()

        # Get button colors based on type
        if button_type == "primary":
            bg_color = colors["primary"]
            fg_color = "#FFFFFF"
        elif button_type == "success":
            bg_color = colors["success"]
            fg_color = "#FFFFFF"
        elif button_type == "error":
            bg_color = colors["error"]
            fg_color = "#FFFFFF"
        elif button_type == "warning":
            bg_color = colors["warning"]
            fg_color = "#000000"
        else:
            bg_color = colors["button_bg"]
            fg_color = colors["fg"]

        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            padx=12,
            pady=6,
            relief=tk.FLAT,
            font=("Arial", 10),
            cursor="hand2",
            **kwargs
        )

        self.button_type = button_type
        self.default_bg = bg_color
        self.hover_color = colors["primary_hover"] if button_type == "primary" else colors["button_hover"]

        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event) -> None:
        """Handle mouse enter."""
        self.config(bg=self.hover_color)

    def _on_leave(self, event) -> None:
        """Handle mouse leave."""
        self.config(bg=self.default_bg)
