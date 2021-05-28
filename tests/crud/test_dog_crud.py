from sqlalchemy.orm import Session

from app import crud
from mock_data.db_test_data import adopted_dogs_dicts
from tests.utils.handle_db_test import HandleDBTest


class TestDogCrud(HandleDBTest):
    def test_get_adopter(sef, db: Session):
        adopted_dogs_out = crud.dog.get_adopted(db)
        for adopted_dog_out in adopted_dogs_out:
            adopted_dog_dict = adopted_dog_out._asdict()
            adopted_dog_dict.pop('id')
            assert adopted_dog_dict in adopted_dogs_dicts
