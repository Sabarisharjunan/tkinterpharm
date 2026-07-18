"""Theme management system."""

from typing import Dict, Tuple, Optional
from enum import Enum


class Theme(Enum):
    """Available themes."""
    LIGHT = "light"
    DARK = "dark"


class ThemeManager:
    """Manages application themes."""

    # Light theme colors
    LIGHT_THEME = {
        "bg": "#F8FAFC",
        "fg": "#1E293B",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "secondary": "#64748B",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444",
        "border": "#E2E8F0",
        "button_bg": "#F1F5F9",
        "button_hover": "#E2E8F0",
        "input_bg": "#FFFFFF",
        "input_border": "#CBD5E1",
        "highlight": "#FEF3C7",
    }

    # Dark theme colors
    DARK_THEME = {
        "bg": "#0F172A",
        "fg": "#F1F5F9",
        "primary": "#3B82F6",
        "primary_hover": "#1D4ED8",
        "secondary": "#CBD5E1",
        "success": "#34D399",
        "warning": "#FBBF24",
        "error": "#F87171",
        "border": "#334155",
        "button_bg": "#1E293B",
        "button_hover": "#334155",
        "input_bg": "#1E293B",
        "input_border": "#475569",
        "highlight": "#1F2937",
    }

    def __init__(self, initial_theme: str = "light"):
        """Initialize theme manager.

        Args:
            initial_theme: Initial theme (light or dark)
        """
        self.current_theme = initial_theme
        self._observers = []

    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors.

        Returns:
            Dictionary of theme colors
        """
        if self.current_theme == "dark":
            return self.DARK_THEME.copy()
        return self.LIGHT_THEME.copy()

    def get_color(self, key: str) -> str:
        """Get specific color from theme.

        Args:
            key: Color key

        Returns:
            Color value
        """
        colors = self.get_colors()
        return colors.get(key, "#000000")

    def set_theme(self, theme: str) -> None:
        """Set current theme.

        Args:
            theme: Theme name (light or dark)
        """
        if theme in ["light", "dark"]:
            self.current_theme = theme
            self._notify_observers()

    def toggle_theme(self) -> str:
        """Toggle between light and dark themes.

        Returns:
            New theme name
        """
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self._notify_observers()
        return self.current_theme

    def subscribe(self, callback) -> None:
        """Subscribe to theme changes.

        Args:
            callback: Callback function
        """
        self._observers.append(callback)

    def _notify_observers(self) -> None:
        """Notify observers of theme change."""
        for callback in self._observers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying observer: {e}")


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager(initial_theme: str = "light") -> ThemeManager:
    """Get global theme manager.

    Args:
        initial_theme: Initial theme if creating new instance

    Returns:
        ThemeManager instance
    """
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager(initial_theme)
    return _theme_manager
