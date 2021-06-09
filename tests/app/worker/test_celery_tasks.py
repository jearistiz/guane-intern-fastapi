from app.worker.celery_tasks import task_post_to_uri


def test_task_post_to_uri():

    task_data = task_post_to_uri()

    assert task_data['status_code'] == 201
    assert task_data['data']
