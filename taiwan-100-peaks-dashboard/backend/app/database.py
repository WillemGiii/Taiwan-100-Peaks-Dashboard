"""Database session management for the FastAPI backend."""

import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


PROJECT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_DIR / ".env")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, future=True) if DATABASE_URL else None
SessionLocal = (
    sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    if engine is not None
    else None
)


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session for request-scoped database access."""

    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

