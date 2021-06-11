from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_db
from tests.mock.db_session import (
    TestSessionLocal,
    testing_get_db,
    setup_test_db,
    teardown_test_db,
)
from tests.utils.security import get_superuser_token_headers


# Setup tests
def pytest_sessionstart(session: pytest.Session):
    setup_test_db()


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session):
    teardown_test_db()


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


@pytest.fixture(scope="function")
def superuser_token_headers(app_client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(app_client)
