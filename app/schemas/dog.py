from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.base_config import ConfigBase


# Shared properties
class DogBase(BaseModel):
    name: Optional[str]
    picture: Optional[str]
    is_adopted: Optional[bool]
    id_user: Optional[int]

    class Config(ConfigBase):
        pass


class DogCreate(DogBase):
    create_date: Optional[datetime] = datetime.utcnow()


class DogUpdate(DogBase):
    pass


# Properties shared by DB models
class DogInDBBase(DogBase):
    id: int
    create_date: datetime
    name: str
    picture: str
    is_adopted: bool
    id_user: Optional[int]

    class Config:
        orm_mode = True


# Properties to return in HTTP response
class Dog(DogInDBBase):
    pass
