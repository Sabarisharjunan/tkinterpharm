"""Application entry point."""

import sys
from pathlib import Path

from app.config import get_config
from app.database import init_db
from app.models import Base
from app.ui.main_window import create_app
from app.utils.logger import get_logger

logger = get_logger(__name__)


def init_database() -> None:
    """Initialize database and create tables."""
    try:
        engine = init_db()
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


def init_directories() -> None:
    """Initialize required directories."""
    dirs = [
        Path("data"),
        Path("data/logs"),
        Path("data/backups"),
        Path("data/exports"),
        Path("config"),
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {dir_path}")


def main() -> None:
    """Main entry point."""
    try:
        logger.info("Starting TkinTermPharm application")

        # Initialize
        init_directories()
        init_database()

        # Create and run app
        app = create_app()
        app.run()

    except Exception as e:
        logger.critical(f"Application initialization failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
