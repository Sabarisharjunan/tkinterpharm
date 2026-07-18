"""SQLAlchemy session management."""

from typing import Optional, Generator

from sqlalchemy.orm import sessionmaker, Session

from app.database.connection import get_engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=None)


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    engine = get_engine()
    SessionLocal.configure(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_session() -> Session:
    """Create a new database session."""
    engine = get_engine()
    SessionLocal.configure(bind=engine)
    return SessionLocal()
