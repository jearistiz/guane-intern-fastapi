from fastapi import APIRouter, Request


users_router = APIRouter()


@users_router.get('/', name='List all users')
async def get_users(request: Request):
    """Get a list of all ``user`` entities.
    """
    return {'hello': 'world'}


@users_router.get('/{name}', name='User info by name')
async def get_users_name(request: Request, name: str):
    """Read one ``user`` entity based on its name
    """
    return {'hello': 'world'}


@users_router.post('/{name}', name='Save user')
async def post_users_name(request: Request, name: str):
    """Save one ``user`` entity.
    """
    return {'hello': 'world'}


@users_router.put('/{name}', name='Update user by name')
async def put_users_name(request: Request, name: str):
    """Update one ``user`` entity based on its name.
    """
    return {'hello': 'world'}


@users_router.delete('/{name}', name='Delete user by name')
async def delete_users_name(request: Request, name: str):
    """Delete one ``user`` entity based on its name.
    """
    return {'hello': 'world'}
