"""Database connection management."""

from typing import Optional

from sqlalchemy import create_engine, Engine, event
from sqlalchemy.pool import QueuePool

from app.config import get_config
from app.utils.logger import get_logger

logger = get_logger(__name__)

_engine: Optional[Engine] = None


def init_db() -> Engine:
    """Initialize database engine."""
    global _engine

    if _engine is not None:
        return _engine

    config = get_config()
    database_url = config.database_url

    logger.info(f"Initializing database: {database_url}")

    if database_url.startswith("sqlite"):
        _engine = create_engine(
            database_url,
            echo=config.get("database.echo", False),
            connect_args={"check_same_thread": False},
        )

        @event.listens_for(_engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    else:
        _engine = create_engine(
            database_url,
            echo=config.get("database.echo", False),
            poolclass=QueuePool,
            pool_size=config.get("database.pool_size", 5),
            max_overflow=config.get("database.max_overflow", 10),
        )

    logger.info("Database initialized successfully")
    return _engine


def get_engine() -> Engine:
    """Get database engine."""
    global _engine
    if _engine is None:
        init_db()
    return _engine
