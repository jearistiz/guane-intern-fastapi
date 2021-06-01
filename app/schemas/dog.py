from datetime import datetime
from typing import List, Optional

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
    id: Optional[int]
    create_date: Optional[datetime] = datetime.utcnow()
    name: str
    picture: Optional[str]
    is_adopted: Optional[bool]
    id_user: Optional[int]

    class Config:
        orm_mode = True


# Properties to return in HTTP response
class Dog(DogInDBBase):
    pass


class Dogs(BaseModel):
    dogs: List[Dog]


class AdoptedDogs(BaseModel):
    adopted_dogs: List[Dog]
