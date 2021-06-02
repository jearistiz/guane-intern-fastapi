from typing import Dict

from fastapi.testclient import TestClient

from app.config import sttgs


def get_superuser_token_headers(app_client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": sttgs['FIRST_SUPERUSER'],
        "password": sttgs['FIRST_SUPERUSER_PASSWORD'],
    }
    r = app_client.post(f"{sttgs['TOKEN_URI']}", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
