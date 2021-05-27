from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import sttgs


test_engine = create_engine(
    sttgs.get('PGDATA_TESTS'),
    pool_pre_ping=True,
    echo=True
)


TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)
