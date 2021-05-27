from app.models import Base
from app.db.init_db import init_db
from tests.mock.db_session import test_engine


if __name__ == '__main__':
    init_db(engine=test_engine)
    Base.metadata.drop_all(bind=test_engine)
