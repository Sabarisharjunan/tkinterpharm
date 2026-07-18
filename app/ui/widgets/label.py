"""Custom themed label."""

import tkinter as tk
from typing import Optional

from app.ui.theme_manager import get_theme_manager


class ThemedLabel(tk.Label):
    """Custom themed label."""

    def __init__(
        self,
        parent: tk.Widget = None,
        text: str = "",
        style: str = "normal",
        **kwargs
    ):
        """Initialize themed label.

        Args:
            parent: Parent widget
            text: Label text
            style: Label style (normal, header, small)
            **kwargs: Additional keyword arguments
        """
        theme_manager = get_theme_manager()
        colors = theme_manager.get_colors()

        # Apply style
        if style == "header":
            font = ("Arial", 14, "bold")
        elif style == "small":
            font = ("Arial", 8)
        else:
            font = ("Arial", 10)

        super().__init__(
            parent,
            text=text,
            bg=colors["bg"],
            fg=colors["fg"],
            font=font,
            **kwargs
        )
