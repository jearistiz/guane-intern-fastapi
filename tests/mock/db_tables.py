from app import crud
from .db_test_data import dogs_mock, users_mock
from .db_session import TestSessionLocal


def populate_dog_table() -> None:
    with TestSessionLocal() as db:
        for dog_in in dogs_mock:
            crud.dog.create(db, obj_in=dog_in)


def populate_user_table() -> None:
    with TestSessionLocal() as db:
        for user_in in users_mock:
            crud.user.create(db, obj_in=user_in)
