"""Custom themed frame."""

import tkinter as tk
from typing import Optional

from app.ui.theme_manager import get_theme_manager


class ThemedFrame(tk.Frame):
    """Custom themed frame."""

    def __init__(
        self,
        parent: tk.Widget = None,
        padded: bool = False,
        **kwargs
    ):
        """Initialize themed frame.

        Args:
            parent: Parent widget
            padded: Whether to add padding
            **kwargs: Additional keyword arguments
        """
        theme_manager = get_theme_manager()
        colors = theme_manager.get_colors()

        super().__init__(
            parent,
            bg=colors["bg"],
            **kwargs
        )

        if padded:
            self.pack(padx=16, pady=16, fill="both", expand=True)
