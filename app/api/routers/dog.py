from fastapi import APIRouter, Request


dog_router = APIRouter()


@dog_router.get('/')
async def hello(request: Request):
    return {'hello': 'world'}
