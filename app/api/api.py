from fastapi import APIRouter

from app.api.routers import dog, user

api_router = APIRouter()
api_router.include_router(dog.dog_router, prefix='/dog', tags=['dog'])
api_router.include_router(user.user_router, prefix='/user', tags=['user'])
