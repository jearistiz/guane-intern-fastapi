from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app import schemas
from app.config import sttgs
from app.worker.celery_tasks import task_post_to_uri


tasks_router = APIRouter()


@tasks_router.post('/celery_task', response_model=schemas.CeleryTaskResponse)
def celery_task(task_complexity: int, request: Request) -> Any:
    response = {
        'task_complexity': task_complexity
    }
    query_uri = (
        sttgs.get('GUANE_WORKER_URI') + f'?task_complexity={task_complexity}'
    )
    try:
        task_post_to_uri.delay(query_uri=query_uri) # noqa
    except Exception:
        response['success'] = False
        response['status'] = 'Internal server error'
        raise HTTPException(status_code=500, detail=response)

    return response


@tasks_router.post(
    '/celery_task_not_async',
    response_model=schemas.CeleryTaskResponse
)
def celery_task_not_async(task_complexity: int, request: Request) -> Any:
    """Same functionality as last endpoint but this one returns the external
    server (guane's) response completely at the expense of loosing the async
    property of celery because of the call to ``task_result.get()``. Keep in
    mind that a request to this endpoint will take at least as many seconds as
    the ``task_complexity`` query parameter.

    This one is just for fun, and to test that guane's server is getting the
    request and giving us an appropriate response.

    Do not use a query parameter greater than 9, since the endpoint calls
    internally ``task_result.get(timeout=10)`` and it would result in a server
    error.
    """
    response = {
        'task_complexity': task_complexity
    }
    query_uri = (
        sttgs.get('GUANE_WORKER_URI') + f'?task_complexity={task_complexity}'
    )
    try:
        task_result = task_post_to_uri.delay(query_uri=query_uri) # noqa
        # Uncomment the following to get detail of guane's server response
        # but lose async call of task
        ext_server_response = task_result.get(timeout=10)
        if ext_server_response:
            response['server_message'] = ext_server_response
    except Exception:
        response['success'] = False
        response['status'] = 'Internal server error'
        raise HTTPException(status_code=500, detail=response)

    return response
