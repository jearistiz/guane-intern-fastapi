from fastapi import APIRouter

from app.config import sttgs
from app.api.routers import (
    dogs_router,
    users_router,
    upload_file_router,
    security_router,
    tasks_router
)


api_router = APIRouter()


api_router.include_router(
    security_router,
    prefix=sttgs.get('SECURITY_PREFIX', '/security'),
    tags=['security']
)
api_router.include_router(
    tasks_router,
    prefix=sttgs.get('CELERY_TASKS_PREFIX', '/tasks'),
    tags=['celery tasks']
)
api_router.include_router(
    dogs_router,
    prefix=sttgs.get('DOGS_API_PREFIX', '/dogs'),
    tags=['dogs']
)
api_router.include_router(
    users_router,
    prefix=sttgs.get('USERS_API_PREFIX', '/dogs'),
    tags=['users']
)
api_router.include_router(
    upload_file_router,
    prefix=sttgs.get('UPLOAD_API_PREFIX', '/upload'),
    tags=['upload file']
)
