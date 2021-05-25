from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import sttgs
from app.db.base_class import Base
from app.db import base  # noqa


# Creates connection to PostgreSQL
engine = create_engine(
    sttgs.get('PGDATA'),
    pool_pre_ping=True,
    echo=True
)

# Create a local session maker to interact with the db via ORM
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """Creates all database tables if they don't already exist.
    """

    Base.metadata.create_all(bind=engine)
