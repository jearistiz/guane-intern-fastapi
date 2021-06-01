from sqlalchemy.orm import Session

from app import crud
from app.models import User
from app.schemas import UserUpdate, UserCreate
from mock_data.db_test_data import users_mock_dicts, users_mock
from tests.utils.handle_db_test import HandleDBTest
from tests.utils.parse_dict import update_dict_fmt_item


class TestUserCrud(HandleDBTest):

    def test_get(self, db: Session):
        user_out = crud.user.get(db, id=1)
        user_compare = user_out._asdict()
        user_compare.pop('id')
        update_dict_fmt_item(user_compare, 'create_date', str)
        assert user_compare in users_mock_dicts

    def test_get_by_name(self, db: Session):
        name = users_mock_dicts[0]['name']
        user_out = crud.user.get_by_name(db, name_in=name)
        assert isinstance(user_out, User), f'{name} is supposed to be in db'
        user_compare = user_out._asdict()
        user_compare.pop('id')
        update_dict_fmt_item(user_compare, 'create_date', str)
        assert user_compare in users_mock_dicts

    def test_get_multi(self, db: Session):
        users_out = crud.user.get_multi(db)
        for user_out in users_out:
            user_compare = user_out._asdict()
            user_compare.pop('id')
            update_dict_fmt_item(user_compare, 'create_date', str)
            assert user_compare in users_mock_dicts

    def test_create(self, db: Session):
        user = users_mock[0]
        created_obj = crud.user.create(db, obj_in=user)
        created_obj_dict = created_obj._asdict()
        created_obj_dict.pop('id')
        assert created_obj_dict == user.dict(exclude_unset=True)
        crud.user.remove(db, id=created_obj.id)

    def test_update(self, db: Session):
        user_id = 1
        updated_last_name = 'Analytics'
        obj = crud.user.get(db, id=user_id)
        updated_obj_info = obj._asdict()
        updated_obj_info.update({'last_name': updated_last_name})
        obj_in = UserUpdate(**updated_obj_info)
        updated_obj = crud.user.update(db, db_obj=obj, obj_in=obj_in)
        assert updated_obj.id == user_id
        assert updated_obj.last_name == updated_last_name

    def test_update_by_name(self, db: Session):
        user_name = users_mock_dicts[0]['name']
        user_obj = crud.user.get_by_name(db, name_in=user_name)
        updated_last_name = 'Analytics'
        updated_obj_info = user_obj._asdict()
        updated_obj_info.update({'last_name': updated_last_name})
        obj_in = UserUpdate(**updated_obj_info)
        updated_obj = crud.user.update_by_name(
            db, name_in_db=user_name, obj_in=obj_in
        )
        assert updated_obj.id == user_obj.id
        assert updated_obj.last_name == updated_last_name

    def test_remove(self, db: Session):
        user_id = 3
        deleted_user = crud.user.remove(db, id=user_id)
        assert deleted_user.id == user_id
        crud.user.create(db, obj_in=UserCreate(**deleted_user._asdict()))

    def test_remove_one_by_name(self, db: Session):
        user_name = users_mock_dicts[3]['name']
        deleted_user = crud.user.remove_one_by_name(db, name=user_name)
        assert deleted_user.name == user_name
        crud.user.create(db, obj_in=UserCreate(**deleted_user._asdict()))
