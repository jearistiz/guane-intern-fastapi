from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import UserCreate, UserUpdate
from app.models import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


user = CRUDUser(User)
