from typing import List

from app import crud
from app.schemas import DogInDBBase, UserInDBBase
from app.db.session import SessionLocal
from mock_data.db_test_data import dogs_mock, users_mock


def populate_dog_table(
    Session=SessionLocal,
    *,
    dogs_in: List[DogInDBBase] = dogs_mock
) -> None:
    with Session() as db:
        for dog_in in dogs_in:
            crud.dog.create(db, obj_in=dog_in)


def populate_user_table(
    Session=SessionLocal,
    *,
    users_in: List[UserInDBBase] = users_mock
) -> None:
    with Session() as db:
        for user_in in users_in:
            crud.user.create(db, obj_in=user_in)


def populate_tables_mock_data(
    populate: bool = False,
    Session=SessionLocal,
    dogs_in: List[DogInDBBase] = dogs_mock,
    users_in: List[UserInDBBase] = users_mock
) -> None:
    """Populates database table with mock data.
    """
    if populate:
        populate_user_table(Session, users_in=users_in)
        populate_dog_table(Session, dogs_in=dogs_in)
