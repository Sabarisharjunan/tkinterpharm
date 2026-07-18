"""Application configuration management."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


class Config:
    """Central configuration manager."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir or Path("config")
        self.data_dir = Path("data")
        self._config: Dict[str, Any] = {}

        load_dotenv()
        self._load_yaml_configs()
        self._set_defaults()

    def _load_yaml_configs(self) -> None:
        """Load all YAML configuration files."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
            return

        for yaml_file in self.config_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r") as f:
                    config = yaml.safe_load(f) or {}
                    self._config.update(config)
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")

    def _set_defaults(self) -> None:
        """Set default configuration values."""
        defaults = {
            "app": {
                "name": "TkinTermPharm",
                "version": "1.0.0",
                "debug": os.getenv("DEBUG", "False").lower() == "true",
                "theme": os.getenv("THEME", "light"),
            },
            "database": {
                "url": os.getenv("DATABASE_URL", "sqlite:///data/database.sqlite"),
                "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
                "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
                "echo": os.getenv("DB_ECHO", "False").lower() == "true",
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "file": str(self.data_dir / "logs" / "app.log"),
                "max_bytes": 10485760,
                "backup_count": 5,
            },
            "security": {
                "password_min_length": 8,
                "session_timeout_minutes": 30,
                "max_login_attempts": 5,
                "lockout_minutes": 15,
            },
            "ui": {
                "window_width": 1200,
                "window_height": 800,
                "font_family": "Segoe UI" if os.name == "nt" else "Arial",
                "font_size_normal": 10,
                "font_size_header": 14,
            },
        }

        for key, value in defaults.items():
            if key not in self._config:
                self._config[key] = value
            elif isinstance(value, dict):
                self._config[key] = {**value, **self._config.get(key, {})}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'app.name')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation.

        Args:
            key: Configuration key
            value: Value to set
        """
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    @property
    def database_url(self) -> str:
        """Get database URL."""
        return self.get("database.url", "sqlite:///data/database.sqlite")

    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get("app.debug", False)

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get("logging.level", "INFO")


def get_config() -> Config:
    """Get global configuration instance.

    Returns:
        Configuration instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

_config_instance = None
