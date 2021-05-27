from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.models.base_class import Base


class Dog(Base):
    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, index=True)
    name = Column(String, index=True)
    picture = Column(String, index=True)
    is_adopted = Column(Boolean, index=True)
    id_user = Column(Integer, ForeignKey('user.id'))

    # ORM relationship between Dog and User entity
    user = relationship('User', back_populates='dogs')
