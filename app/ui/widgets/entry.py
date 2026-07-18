"""Custom themed entry field."""

import tkinter as tk
from typing import Optional

from app.ui.theme_manager import get_theme_manager


class ThemedEntry(tk.Frame):
    """Custom themed entry field with label."""

    def __init__(
        self,
        parent: tk.Widget = None,
        label: str = "",
        placeholder: str = "",
        show: str = None,
        **kwargs
    ):
        """Initialize themed entry.

        Args:
            parent: Parent widget
            label: Label text
            placeholder: Placeholder text
            show: Character to show for password fields
            **kwargs: Additional keyword arguments
        """
        theme_manager = get_theme_manager()
        colors = theme_manager.get_colors()

        super().__init__(parent, bg=colors["bg"], **kwargs)

        self.theme_manager = theme_manager
        self.colors = colors
        self.placeholder = placeholder
        self.show = show
        self._has_placeholder = False

        # Label
        if label:
            label_widget = tk.Label(
                self,
                text=label,
                bg=colors["bg"],
                fg=colors["fg"],
                font=("Arial", 10),
            )
            label_widget.pack(anchor="w", pady=(0, 4))

        # Entry
        self.entry = tk.Entry(
            self,
            bg=colors["input_bg"],
            fg=colors["fg"],
            insertbackground=colors["primary"],
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 10),
            show=show,
        )
        self.entry.pack(fill="x")

        # Add placeholder if provided
        if placeholder:
            self.entry.insert(0, placeholder)
            self._has_placeholder = True
            self.entry.config(fg=colors["border"])
            self.entry.bind("<FocusIn>", self._on_focus_in)
            self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event) -> None:
        """Handle focus in."""
        if self._has_placeholder and self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.colors["fg"])
            self._has_placeholder = False

    def _on_focus_out(self, event) -> None:
        """Handle focus out."""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.colors["border"])
            self._has_placeholder = True

    def get(self) -> str:
        """Get entry value.

        Returns:
            Entry value
        """
        value = self.entry.get()
        if self._has_placeholder and value == self.placeholder:
            return ""
        return value

    def set(self, value: str) -> None:
        """Set entry value.

        Args:
            value: Value to set
        """
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, value)
            self.entry.config(fg=self.colors["fg"])
            self._has_placeholder = False
        else:
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.colors["border"])
            self._has_placeholder = True

    def clear(self) -> None:
        """Clear entry value."""
        self.set("")
