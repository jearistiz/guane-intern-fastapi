from app.config import sttgs


def task_uri(specific_endpoint: str, task_complexity: int = 0) -> str:
    return (
        sttgs.get('API_PREFIX')
        + sttgs.get('CELERY_TASKS_PREFIX')
        + specific_endpoint
        + '?task_complexity='
        + str(task_complexity)
    )
