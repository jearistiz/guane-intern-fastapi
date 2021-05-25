from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base


class Dog(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    picture = Column(String, index=True)
    is_adopted = Column(Boolean, index=True)
    create_date = Column(Date, index=True)
    id_user = Column(Integer, ForeignKey('user.id'))

    # ORM relationship between Dog and User entity
    owner = relationship('User', back_populates='dogs')
