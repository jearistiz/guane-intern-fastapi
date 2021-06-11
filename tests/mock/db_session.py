from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import sttgs
from app.db.db_manager import create_all_tables, drop_all_tables
from app.db.utils.populate_tables import populate_tables_mock_data
from mock_data.db_test_data import dogs_mock, users_mock


test_engine = create_engine(
    sttgs.get('POSTGRES_TESTS_URI'),
    pool_pre_ping=True,
    echo=True
)


TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def populate_test_tables() -> None:
    # Populate tables with test db data
    populate_tables_mock_data(
        populate=True,
        Session=TestSessionLocal,
        dogs_in=dogs_mock,
        users_in=users_mock
    )


def setup_test_db() -> None:
    drop_all_tables(engine=test_engine, drop=True)
    create_all_tables(engine=test_engine)
    populate_test_tables()


def teardown_test_db() -> None:
    drop_all_tables(engine=test_engine, drop=True)


def testing_get_db() -> Generator:
    """For some reason, app.dependency_overrides does not accept pytest
    fixtures as overrider, so this function is needed although it is exactlythe
    same as db
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
