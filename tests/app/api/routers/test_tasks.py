from typing import Dict

from fastapi.testclient import TestClient

from tests.utils.uri import task_uri


def test_celery_task(
    app_client: TestClient,
    superuser_token_headers: Dict[str, str]
):
    task_complexity = 0
    response = app_client.post(
        task_uri('/celery_task', task_complexity),
        headers=superuser_token_headers
    )
    assert response.status_code == 201
    content = response.json()
    assert content['task_complexity'] == task_complexity
    assert content["status"]
    assert content['server_message'] is None
    assert content['success'] is True
