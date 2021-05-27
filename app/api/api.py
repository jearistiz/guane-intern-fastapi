from fastapi import APIRouter

from app.api.routers import dogs_router, users_router

api_router = APIRouter()
api_router.include_router(dogs_router, prefix='/dogs', tags=['dogs'])
api_router.include_router(users_router, prefix='/users', tags=['users'])
