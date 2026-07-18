"""Custom message dialog."""

import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional


class Dialog(tk.Toplevel):
    """Custom dialog base class."""

    def __init__(
        self,
        parent: tk.Widget = None,
        title: str = "Dialog",
        **kwargs
    ):
        """Initialize dialog.

        Args:
            parent: Parent widget
            title: Dialog title
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.result = None

    def center_window(self) -> None:
        """Center window on parent."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class MessageDialog(Dialog):
    """Simple message dialog."""

    def __init__(
        self,
        parent: tk.Widget = None,
        title: str = "Message",
        message: str = "",
        dialog_type: str = "info",
    ):
        """Initialize message dialog.

        Args:
            parent: Parent widget
            title: Dialog title
            message: Message text
            dialog_type: Type of dialog (info, warning, error, success)
        """
        super().__init__(parent, title=title)

        # Message label
        label = tk.Label(
            self,
            text=message,
            wraplength=300,
            padx=20,
            pady=20,
        )
        label.pack()

        # OK button
        button = tk.Button(
            self,
            text="OK",
            command=self.destroy,
            padx=20,
            pady=10,
        )
        button.pack(pady=10)

        self.center_window()
        self.wait_window()


def show_info(parent: tk.Widget, title: str, message: str) -> None:
    """Show info dialog."""
    messagebox.showinfo(title, message, parent=parent)


def show_warning(parent: tk.Widget, title: str, message: str) -> None:
    """Show warning dialog."""
    messagebox.showwarning(title, message, parent=parent)


def show_error(parent: tk.Widget, title: str, message: str) -> None:
    """Show error dialog."""
    messagebox.showerror(title, message, parent=parent)


def ask_yes_no(parent: tk.Widget, title: str, message: str) -> bool:
    """Show yes/no dialog."""
    return messagebox.askyesno(title, message, parent=parent)


def ask_ok_cancel(parent: tk.Widget, title: str, message: str) -> bool:
    """Show ok/cancel dialog."""
    return messagebox.askokcancel(title, message, parent=parent)
