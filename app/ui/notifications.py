"""Notification/Toast widget."""

import tkinter as tk
from typing import Optional
from datetime import datetime, timedelta

from app.ui.theme_manager import get_theme_manager


class Toast(tk.Toplevel):
    """Toast notification widget."""

    def __init__(
        self,
        parent: tk.Widget = None,
        message: str = "",
        title: str = "",
        toast_type: str = "info",
        duration: int = 3000,
    ):
        """Initialize toast notification.

        Args:
            parent: Parent widget
            message: Message text
            title: Message title
            toast_type: Type (info, success, warning, error)
            duration: Duration in milliseconds
        """
        super().__init__(parent)
        self.withdraw()
        self.attributes("-topmost", True)
        self.resizable(False, False)

        theme_manager = get_theme_manager()
        colors = theme_manager.get_colors()

        # Get colors based on type
        type_colors = {
            "success": colors["success"],
            "error": colors["error"],
            "warning": colors["warning"],
            "info": colors["primary"],
        }
        bg_color = type_colors.get(toast_type, colors["primary"])

        # Main frame
        main_frame = tk.Frame(
            self,
            bg=bg_color,
            padx=16,
            pady=12,
        )
        main_frame.pack(fill="both", expand=True)

        # Title
        if title:
            title_label = tk.Label(
                main_frame,
                text=title,
                bg=bg_color,
                fg="#FFFFFF",
                font=("Arial", 11, "bold"),
            )
            title_label.pack(anchor="w")

        # Message
        message_label = tk.Label(
            main_frame,
            text=message,
            bg=bg_color,
            fg="#FFFFFF",
            font=("Arial", 10),
            wraplength=300,
        )
        message_label.pack(anchor="w")

        self.geometry(f"350x+{parent.winfo_screenwidth() - 370}+30")
        self.deiconify()

        # Auto-close after duration
        self.after(duration, self.destroy)


def show_toast(
    parent: tk.Widget,
    message: str,
    title: str = "",
    toast_type: str = "info",
    duration: int = 3000,
) -> None:
    """Show toast notification.

    Args:
        parent: Parent widget
        message: Message text
        title: Message title
        toast_type: Type (info, success, warning, error)
        duration: Duration in milliseconds
    """
    Toast(parent, message, title, toast_type, duration)
