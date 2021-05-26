from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps


users_router = APIRouter()


@users_router.get('/', name='List all users')
async def get_users(db: Session = Depends(deps.get_db)) -> Any:
    """Get a list of all ``user`` entities.
    """
    return {'hello': 'world'}


@users_router.get('/{name}', name='User info by name')
async def get_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Read one ``user`` entity based on its name
    """
    return {'hello': 'world'}


@users_router.post('/{name}', name='Save user')
async def post_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Save one ``user`` entity.
    """
    return {'hello': 'world'}


@users_router.put('/{name}', name='Update user by name')
async def put_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Update one ``user`` entity based on its name.
    """
    return {'hello': 'world'}


@users_router.delete('/{name}', name='Delete user by name')
async def delete_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Delete one ``user`` entity based on its name.
    """
    return {'hello': 'world'}
