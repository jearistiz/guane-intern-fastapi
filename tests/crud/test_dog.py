from sqlalchemy.orm import Session

from app import crud
from ..mock.db_test_data import dog_mock_dicts


def test_get_dog(db: Session):
    dogs_out = crud.dog.get_multi(db)
    for dog_out in dogs_out:
        dog_compare = dog_out._asdict()
        dog_compare.pop('id')
        print(dog_compare)
        print(dog_mock_dicts)
        assert dog_compare in dog_mock_dicts
