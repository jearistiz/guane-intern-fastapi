from fastapi import APIRouter, Request


dogs_router = APIRouter()


@dogs_router.get('/', name='List of all dogs\' info.')
async def dogs(request: Request):
    """Get a list of all dog entities.
    """
    return {'hello': 'world'}


@dogs_router.get('/{name}', name='Dog info by name.')
async def get_dogs_name(request: Request, name: str):
    """Read one ``dog`` entity based on its name
    """
    return {'hello': 'world'}


@dogs_router.get('/is_adopted', name='Adopted dogs\' info.')
async def get_dogs_is_adopted(request: Request):
    """Get a list of all ``dog`` entities where the flag ``is_adopted`` is
    True.
    """
    return {'hello': 'world'}


@dogs_router.post('/{name}', name='Save one dog.')
async def post_dogs_name(request: Request, name: str):
    """Save one ``dog`` entity.
    """
    return {'hello': 'world'}


@dogs_router.put('/{name}', name='Update dog info by name.')
async def put_dogs_name(request: Request, name: str):
    """Update one ``dog`` entity based on its name.
    """
    return {'hello': 'world'}


@dogs_router.delete('/{name}', name='Delete dog by name.')
async def delete_dogs_name(request: Request, name: str):
    """Delete one ``dog`` entity based on its name.
    """
    return {'hello': 'world'}
