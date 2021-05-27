from app.models import Base
from app.db.session import engine
from app.db.init_db import init_db


if __name__ == '__main__':
    init_db()
    Base.metadata.drop_all(bind=engine)
