"""Screen base class."""

import tkinter as tk
from typing import Optional

from app.ui.widgets.frame import ThemedFrame


class BaseScreen(ThemedFrame):
    """Base screen class."""

    def __init__(
        self,
        parent: tk.Widget = None,
        name: str = "Screen",
        **kwargs
    ):
        """Initialize base screen.

        Args:
            parent: Parent widget
            name: Screen name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        self.name = name
        self.pack(fill="both", expand=True)

    def on_enter(self) -> None:
        """Called when screen is shown."""
        pass

    def on_exit(self) -> None:
        """Called when screen is hidden."""
        pass

    def refresh(self) -> None:
        """Refresh screen data."""
        pass
