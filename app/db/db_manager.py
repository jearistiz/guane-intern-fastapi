from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from app.config import sttgs
from app.models.base_class import Base
# We need to import base in order to appropriately create all database tables
# using init_bd() function
from app.db import base  # noqa


# Creates connection to PostgreSQL
engine = create_engine(
    sttgs.get('PGDATA'),
    pool_pre_ping=True,
    echo=True
)


# Create a local session maker to interact with the db via ORM
def SessionLocal(engine: Engine = engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def init_db(engine: Engine = engine):
    """Creates all database tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)
