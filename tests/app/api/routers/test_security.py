from typing import Dict

from fastapi.testclient import TestClient

from app.config import sttgs


def test_post_login_for_access_token(app_client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": sttgs['FIRST_SUPERUSER'],
        "password": sttgs['FIRST_SUPERUSER_PASSWORD'],
    }
    r = app_client.post(f"{sttgs['TOKEN_URI']}", data=login_data)
    tokens = r.json()
    assert tokens['access_token']
    assert tokens['token_type']
