from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class SuperUser(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class SuperUserInDB(SuperUser):
    hashed_password: str
