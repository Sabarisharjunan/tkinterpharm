"""User management screen."""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Callable

from app.ui.widgets.frame import ThemedFrame
from app.ui.widgets.label import ThemedLabel
from app.ui.widgets.button import ThemedButton
from app.ui.widgets.entry import ThemedEntry
from app.ui.dialogs import show_info, show_error, ask_yes_no
from app.services.user_service import UserService
from app.models.user import User
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UserManagementScreen(ThemedFrame):
    """User management screen."""

    def __init__(
        self,
        parent: tk.Widget = None,
        user_service: UserService = None,
        **kwargs
    ):
        """Initialize user management screen.

        Args:
            parent: Parent widget
            user_service: User service instance
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        self.user_service = user_service
        self.users: List[User] = []
        self._create_widgets()
        self.refresh()

    def _create_widgets(self) -> None:
        """Create user management widgets."""
        # Header
        header_frame = ThemedFrame(self)
        header_frame.pack(fill="x", padx=16, pady=16)

        title = ThemedLabel(
            header_frame,
            text="User Management",
            style="header",
        )
        title.pack(anchor="w")

        # Toolbar
        toolbar_frame = ThemedFrame(self)
        toolbar_frame.pack(fill="x", padx=16, pady=(0, 16))

        search_label = ThemedLabel(toolbar_frame, text="Search:")
        search_label.pack(side="left", padx=(0, 8))

        self.search_entry = ThemedEntry(
            toolbar_frame,
            placeholder="Search users...",
        )
        self.search_entry.pack(side="left", padx=(0, 16), fill="x", expand=True)

        add_btn = ThemedButton(
            toolbar_frame,
            text="+ Add User",
            command=self._on_add_user,
            button_type="primary",
        )
        add_btn.pack(side="left", padx=4)

        refresh_btn = ThemedButton(
            toolbar_frame,
            text="Refresh",
            command=self.refresh,
        )
        refresh_btn.pack(side="left", padx=4)

        # User table
        table_frame = ThemedFrame(self)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Create treeview
        columns = ("ID", "Username", "Email", "Name", "Role", "Status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=15,
            show="headings",
        )

        # Define column headings and widths
        for col in columns:
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        # Context menu
        self.tree.bind("<Button-3>", self._on_tree_right_click)

    def _on_add_user(self) -> None:
        """Handle add user button click."""
        show_info(self, "Add User", "Add user feature coming soon!")

    def _on_tree_right_click(self, event) -> None:
        """Handle right click on tree."""
        item = self.tree.selection()
        if not item:
            return

        # Get user data
        values = self.tree.item(item, "values")
        user_id = int(values[0])

        # Create context menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self._on_edit_user(user_id))
        menu.add_command(label="Delete", command=lambda: self._on_delete_user(user_id))
        menu.post(event.x_root, event.y_root)

    def _on_edit_user(self, user_id: int) -> None:
        """Handle edit user."""
        show_info(self, "Edit User", f"Edit user {user_id} feature coming soon!")

    def _on_delete_user(self, user_id: int) -> None:
        """Handle delete user."""
        if ask_yes_no(self, "Confirm", "Are you sure you want to deactivate this user?"):
            try:
                self.user_service.deactivate_user(user_id)
                show_info(self, "Success", "User deactivated successfully")
                self.refresh()
            except Exception as e:
                show_error(self, "Error", f"Failed to deactivate user: {str(e)}")

    def refresh(self) -> None:
        """Refresh user list."""
        try:
            self.users = self.user_service.get_all_users(limit=100)
            self._update_tree()
        except Exception as e:
            logger.error(f"Error loading users: {str(e)}")
            show_error(self, "Error", "Failed to load users")

    def _update_tree(self) -> None:
        """Update tree with users."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add users
        for user in self.users:
            status = "Active" if user.is_active else "Inactive"
            self.tree.insert(
                "",
                "end",
                values=(
                    user.id,
                    user.username,
                    user.email,
                    user.full_name,
                    user.role.value,
                    status,
                ),
            )
