from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.db_manager import SessionLocal
from app.main import app


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    pass


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session, exitstatus):
    pass


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def app_client() -> Generator:
    with TestClient(app) as c:
        yield c
