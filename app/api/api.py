from fastapi import APIRouter

from app.config import sttgs
from app.api.routers import dogs_router, users_router

api_router = APIRouter()
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
