from typing import Any, Awaitable, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from celery.result import AsyncResult

from app import schemas
from app.config import sttgs
from app.crud import superuser_crud
from app.worker.celery_app import celery_app


tasks_router = APIRouter()


@tasks_router.post(
    '/celery_task',
    response_model=schemas.CeleryTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def celery_task(
    task_complexity: int,
    request: Request,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    return await run_task_post_to_uri(
        task_complexity=task_complexity,
        get_task_result=False,
    )


@tasks_router.post(
    '/celery_task_not_async',
    response_model=schemas.CeleryTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def celery_task_not_async(
    task_complexity: int,
    request: Request,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
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
    return await run_task_post_to_uri(
        task_complexity=task_complexity,
        get_task_result=True,
        get_result_timeout=10.0
    )


async def run_task_post_to_uri(
    task_complexity: int = 0,
    *,
    get_task_result: bool,
    get_result_timeout: float = 10.0,
) -> Awaitable[Dict[str, Any]]:
    """If ``get_task_result`` is set to ``True``, the async nature of the
    celerymtask will be lost, since we make a call to ``task_result.get``.

    ``get_result_timeout`` only makes sense when ``get_task_result`` is set to
    true. This is the maximum ammount of time the server will wait for the
    task to complete.
    """
    response: Dict[str, Any] = {
        'task_complexity': task_complexity
    }
    query_uri = (
        sttgs.get('GUANE_WORKER_URI') + f'?task_complexity={task_complexity}'
    )
    try:
        task_result: AsyncResult = celery_app.send_task(
            'app.worker.tasks.post_to_uri_task',
            kwargs={'query_uri': query_uri}
        )
        # If next code block is executed, the async nature of the task will
        # be lost since task_result.get waits until the task is complete.
        if get_task_result:
            ext_server_response = task_result.get(timeout=get_result_timeout)
            if ext_server_response:
                response['server_message'] = ext_server_response
    except Exception:
        response['success'] = False
        response['status'] = 'Internal server error'
        raise HTTPException(status_code=500, detail=response)

    return response
