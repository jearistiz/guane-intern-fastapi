from typing import Dict

from fastapi.testclient import TestClient

from tests.utils.uri import task_uri


def assert_post_uri_task(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    specific_endpoint: str,
    task_complexity: int,
    not_async: bool = False
):
    response = client.post(
        task_uri(specific_endpoint, task_complexity),
        headers=superuser_token_headers
    )
    assert response.status_code == 201
    content = response.json()
    assert content['task_complexity'] == task_complexity
    assert content["status"]
    if not_async:
        assert content['server_message']
    else:
        assert content['server_message'] is None
    assert content['success'] is True


def test_celery_task(
    app_client: TestClient,
    superuser_token_headers: Dict[str, str]
):
    assert_post_uri_task(
        app_client, superuser_token_headers,
        specific_endpoint='/celery_task',
        task_complexity=0,
    )


def test_celery_task_not_async(
    app_client: TestClient,
    superuser_token_headers: Dict[str, str]
):
    assert_post_uri_task(
        app_client, superuser_token_headers,
        task_complexity=0,
        specific_endpoint='/celery_task_not_async',
        not_async=True,
    )
