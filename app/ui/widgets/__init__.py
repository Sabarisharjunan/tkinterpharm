"""Base widget class with theme support."""

import tkinter as tk
from typing import Optional, Dict, Any

from app.ui.theme_manager import get_theme_manager


class ThemedWidget(tk.Frame):
    """Base themed widget."""

    def __init__(self, parent: tk.Widget = None, **kwargs):
        """Initialize themed widget.

        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        self.theme_manager = get_theme_manager()
        self._apply_theme()
        self.theme_manager.subscribe(self._on_theme_changed)

    def _apply_theme(self) -> None:
        """Apply theme to widget."""
        colors = self.theme_manager.get_colors()
        self.config(
            bg=colors["bg"],
            fg=colors["fg"],
        )

    def _on_theme_changed(self) -> None:
        """Handle theme change."""
        self._apply_theme()

    def get_color(self, key: str) -> str:
        """Get color from theme.

        Args:
            key: Color key

        Returns:
            Color value
        """
        return self.theme_manager.get_color(key)
