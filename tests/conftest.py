from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.init_db import init_db
from app.models.base_class import Base
from .mock.db_session import TestSessionLocal, test_engine
from .mock.db_tables import populate_dog_table, populate_user_table


# Setup test DB
def pytest_sessionstart(session: pytest.Session):
    # Create all tables
    init_db(engine=test_engine)

    # Populate User table
    populate_user_table()

    # Populate Dog table
    populate_dog_table()


# Delete all tables in test DB
def pytest_sessionfinish(session: pytest.Session, exitstatus):
    # Delete all tables
    Base.metadata.drop_all(test_engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestSessionLocal(engine=test_engine)


@pytest.fixture(scope="module")
def app_client() -> Generator:
    with TestClient(app) as c:
        yield c
