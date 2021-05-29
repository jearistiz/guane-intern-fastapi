from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.config import sttgs


# Creates connection to PostgreSQL
engine = create_engine(
    sttgs.get('POSTGRES_URI'),
    pool_pre_ping=True,
    echo=True
)


# Create a local session maker to interact with the db via ORM
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
