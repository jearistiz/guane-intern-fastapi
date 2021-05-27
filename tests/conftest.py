from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.init_db import init_db
from app.db.utils import populate_dog_table, populate_user_table
from app.models.base_class import Base
from mock_data.db_test_data import dogs_mock, users_mock
from .mock.db_session import TestSessionLocal, test_engine


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    # Create all tables
    init_db(engine=test_engine)

    # Populate User table
    populate_user_table(Session=TestSessionLocal, users_in=users_mock)

    # Populate Dog table
    populate_dog_table(Session=TestSessionLocal, dogs_in=dogs_mock)


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session):
    # Delete all tables
    Base.metadata.drop_all(bind=test_engine)


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
