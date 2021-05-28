from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.db_manager import create_all_tables, drop_all_tables
from app.db.utils import populate_dog_table, populate_user_table
from mock_data.db_test_data import dogs_mock, users_mock
from .mock.db_session import TestSessionLocal, test_engine


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    # Create all tables
    create_all_tables(engine=test_engine)

    # Populate User table
    populate_user_table(Session=TestSessionLocal, users_in=users_mock)

    # Populate Dog table
    populate_dog_table(Session=TestSessionLocal, dogs_in=dogs_mock)


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session):
    drop_all_tables(engine=test_engine, drop=True)


@pytest.fixture(scope="module")
def db() -> Generator:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def app_client() -> Generator:
    with TestClient(app) as c:
        yield c
