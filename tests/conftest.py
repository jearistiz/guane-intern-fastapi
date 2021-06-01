from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_db
from tests.mock.db_session import (
    TestSessionLocal,
    init_test_db,
    testing_get_db,
    close_test_db
)


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    init_test_db()


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session):
    close_test_db()


@pytest.fixture(scope="function")
def db() -> Generator:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def app_client(db) -> Generator:
    app.dependency_overrides[get_db] = testing_get_db
    test_app = TestClient(app)
    with test_app as c:
        yield c
