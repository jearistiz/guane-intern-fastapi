from app.db.db_manager import drop_all_tables
from tests.mock.db_session import test_engine


if __name__ == '__main__':
    drop_all_tables(engine=test_engine, drop=True)
