from app.config import sttgs
from app.utils.http_request import post_to_uri


def test_post_to_uri():
    task_complexity = 0
    task_query_url = (
        sttgs.get('GUANE_WORKER_URI') + f'?task_complexity={task_complexity}'
    )
    response = post_to_uri(
        task_query_url,
        message={'task_complexity': task_complexity}
    )
    assert response.status_code == 201
    assert response.json()['status']
