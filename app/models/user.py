from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)

    # ORM relationship between User and Dog entity
    dogs = relationship('Dog', back_populates='user')
