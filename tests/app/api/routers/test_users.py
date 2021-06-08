from typing import Dict

from fastapi.testclient import TestClient

from app.config import sttgs
from mock_data.db_test_data import users_mock_dicts
from tests.utils.handle_db_test import HandleDBTest


class TestUsersRouter(HandleDBTest):

    users_api_prefix = sttgs.get('API_PREFIX') + sttgs.get('USERS_API_PREFIX')

    def users_name_route(self, name):
        return self.users_api_prefix + '/' + name

    def assert_users_data(self, *, reference: dict, compare: dict):
        assert compare['name'] == reference['name']
        assert compare['email'] == reference['email']
        assert 'create_date' in compare
        assert 'id' in compare

    def test_get_users(self, app_client: TestClient):
        response = app_client.get(self.users_api_prefix)
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content['users'], list)
        users = content['users']
        user_names = [ref_user['name'] for ref_user in users_mock_dicts]
        for user in users:
            assert user['name'] in user_names

    def test_get_users_name(self, app_client: TestClient):
        data = users_mock_dicts[0]
        get_users_name_route = self.users_name_route(data.get('name'))
        response = app_client.get(get_users_name_route, json=data)
        assert response.status_code == 200
        content = response.json()
        self.assert_users_data(reference=data, compare=content)

    def test_post_users_name(
        self, app_client: TestClient, superuser_token_headers: Dict[str, str]
    ) -> None:
        data = users_mock_dicts[0].copy()
        data.update({'name': 'Juan'})
        post_users_name_route = self.users_name_route(data.get('name'))
        response = app_client.post(
            post_users_name_route, json=data, headers=superuser_token_headers
        )
        assert response.status_code == 201
        content = response.json()
        self.assert_users_data(reference=data, compare=content)

    def test_put_users_name(
        self, app_client: TestClient, superuser_token_headers: Dict[str, str]
    ) -> None:
        data = users_mock_dicts[0].copy()
        old_name = data['name']
        data.update({'name': 'Juan'})
        post_users_name_route = self.users_name_route(old_name)
        response = app_client.put(
            post_users_name_route, json=data, headers=superuser_token_headers
        )
        assert response.status_code == 200
        content = response.json()
        self.assert_users_data(reference=data, compare=content)

    def test_delete_users_name(
        self, app_client: TestClient, superuser_token_headers: Dict[str, str]
    ) -> None:
        data = users_mock_dicts[0]
        get_users_name_route = self.users_name_route(data.get('name'))
        response = app_client.delete(
            get_users_name_route, json=data, headers=superuser_token_headers
        )
        assert response.status_code == 200
        content = response.json()
        self.assert_users_data(reference=data, compare=content)
