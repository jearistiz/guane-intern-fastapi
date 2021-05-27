from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base_config import ConfigBase
from app.services.http_request import get_dog_picture_uri


# Shared properties
class DogBase(BaseModel):
    name: Optional[str]
    picture: Optional[str] = get_dog_picture_uri()
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
    picture: str
    is_adopted: bool
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
