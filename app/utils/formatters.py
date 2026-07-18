"""Data formatting utilities."""

from datetime import datetime
from typing import Optional


class Formatters:
    """Data formatting utilities."""

    @staticmethod
    def format_datetime(dt: Optional[datetime], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime object."""
        return dt.strftime(fmt) if dt else "N/A"

    @staticmethod
    def format_date(dt: Optional[datetime], fmt: str = "%Y-%m-%d") -> str:
        """Format date."""
        return dt.strftime(fmt) if dt else "N/A"

    @staticmethod
    def format_currency(amount: float, currency: str = "$") -> str:
        """Format currency."""
        return f"{currency}{amount:,.2f}"

    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number."""
        return f"{value:,.{decimals}f}"

    @staticmethod
    def truncate_string(text: str, length: int = 50, suffix: str = "...") -> str:
        """Truncate string to specified length."""
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix
