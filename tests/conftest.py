from typing import Generator

import pytest
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.config import sttgs
from app.db.db_manager import SessionLocal, init_db
from app.models.base_class import Base
from .utils import dogs


engine = create_engine(
    sttgs.get('PGDATA_TESTS'),
    pool_pre_ping=True,
    echo=True
)


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    # Create all tables
    init_db(engine=engine)

    # Populate Dog table

    # Populate User table


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session, exitstatus):
    # Delete all tables
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def app_client() -> Generator:
    with TestClient(app) as c:
        yield c
