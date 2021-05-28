from fastapi.testclient import TestClient

from app.config import sttgs
from mock_data.db_test_data import dogs_mock_dicts, adopted_dogs_dicts
from tests.mock.db_session import clean_all_test_tables, populate_test_tables


class TestDogsRouter:

    dogs_api_prefix = sttgs.get('API_PREFIX') + sttgs.get('DOGS_API_PREFIX')

    def setup_method(self):
        populate_test_tables()

    def teardown_method(self):
        clean_all_test_tables()

    @classmethod
    def teardown_class():
        populate_test_tables()

    def test_get_dogs(self, app_client: TestClient) -> None:
        response = app_client.get(self.dogs_api_prefix)
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content['dogs'], list)
        dogs = content['dogs']
        dogs_names = [ref_dog['name'] for ref_dog in dogs_mock_dicts]
        for dog in dogs:
            assert dog['name'] in dogs_names

    def test_get_dogs_is_adopted(self, app_client: TestClient) -> None:
        get_dogs_is_adopted_route = self.dogs_api_prefix + '/is_adopted'
        response = app_client.get(get_dogs_is_adopted_route)
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content['adopted_dogs'], list)
        dogs = content['adopted_dogs']
        adopted_dogs_names = [
            ref_dog['name'] for ref_dog in adopted_dogs_dicts
        ]
        for dog in dogs:
            assert dog['is_adopted'] is True
            assert dog['name'] in adopted_dogs_names

    def test_get_dogs_name(self, app_client: TestClient) -> None:
        data = dogs_mock_dicts[0]
        data['create_date'] = str(data['create_date'])
        get_dogs_name_route = self.dogs_api_prefix + '/' + data.get('name')
        response = app_client.post(get_dogs_name_route, json=data)
        assert response.status_code == 200
        content = response.json()
        assert content['name'] == data['name']
        assert content['picture'] == data['picture']
        assert 'create_date' in content
        assert 'id' in content
        assert 'picture' in content
        assert 'is_adopted' in content
        assert 'id_user' in content

    def test_post_dogs_name(self, app_client: TestClient) -> None:
        data = dogs_mock_dicts[0].copy()
        old_name = data['name']
        data.update({'name': 'Juan'})
        data['create_date'] = str(data['create_date'])
        post_dogs_name_route = self.dogs_api_prefix + '/' + data.get('name')
        response = app_client.post(post_dogs_name_route, json=data)
        assert response.status_code == 200
        content = response.json()
        assert content['name'] == data['name']
        assert content['picture'] == data['picture']
        assert 'create_date' in content
        assert 'id' in content
        assert 'picture' in content
        assert 'is_adopted' in content
        assert 'id_user' in content
        # Revert test database to previous status
        data.update({'name': old_name})
        response2 = app_client.post(post_dogs_name_route, json=data)
        assert response2.status_code == 200

    def test_put_dogs_name(self, app_client: TestClient) -> None:
        ...

    def test_delete_dogs_name(self, app_client: TestClient) -> None:
        ...
