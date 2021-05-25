from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from app.config import sttgs
from app.db.base_class import Base


# Creates connection to PostgreSQL
db_engine = create_engine(
    sttgs.get('PGDATA'),
    connect_args={"check_same_thread": False},
    echo=True
)

# Create a local session maker to interact with the db via ORM
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=db_engine
)


def init_db(engine: Engine = db_engine):
    """Creates all database tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)
