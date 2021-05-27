from sqlalchemy.engine import Engine

from app.models.base_class import Base
# We need to import app.db.base in order to appropriately create all database
# tables using init_bd() function
from app.db import base  # noqa
from app.db.session import engine


def create_all_tables(engine: Engine = engine):
    """Creates all database tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)


def drop_all_tables(engine: Engine = engine, *, drop: bool):
    if drop:
        Base.metadata.drop_all(bind=engine)
