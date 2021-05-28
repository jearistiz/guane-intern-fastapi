from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.base_config import ConfigBase


# Shared properties
class UserBase(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

    class Config(ConfigBase):
        pass


class UserCreate(UserBase):
    create_date: Optional[datetime] = datetime.utcnow()


class UserUpdate(UserBase):
    pass


# Properties shared by DB models
class UserInDBBase(UserBase):
    id: Optional[int]
    create_date: Optional[datetime] = datetime.utcnow()
    name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


# Properties to return in HTTP response
class User(UserInDBBase):
    pass


class Users(BaseModel):
    users: List[User]
