from app.worker.tasks import post_to_uri_task


def test_task_post_to_uri():

    task_data = post_to_uri_task()

    assert task_data['status_code'] == 201
    assert task_data['data']
