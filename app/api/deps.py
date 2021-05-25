from typing import Generator
from app.db.db_manager import SessionLocal


def get_db() -> Generator:
    """Starts and ends session in each route that needs database access.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
