from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.crud import superuser_crud


users_router = APIRouter()

# Web crud was implemented as a wrapper to avoid duplicate code between
# the two main routers (dogs, users)
user_web_crud = crud.WebCRUDWrapper(crud.user, enty_name='user')


@users_router.get(
    '/',
    response_model=schemas.Users,
    name='List all users',
)
async def get_users(
    db: Session = Depends(deps.get_db)
) -> Any:
    return user_web_crud.get_all_entries(db)


@users_router.get(
    '/{name}',
    response_model=schemas.User,
    name='User info by name'
)
async def get_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Read one ``user`` entity based on its name.
    """
    return user_web_crud.get_enty_by_name(db, name)


@users_router.post(
    '/{name}',
    response_model=schemas.User,
    name='Create user',
    status_code=status.HTTP_201_CREATED,
)
async def post_users_name(
    *,
    db: Session = Depends(deps.get_db),
    user_info: schemas.UserCreate,
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """Save one ``user`` entity.
    """
    return user_web_crud.post_enty_by_name(db, name=name, enty_info=user_info)


@users_router.put(
    '/{name}',
    response_model=schemas.User,
    name='Update user by name'
)
async def put_users_name(
    *,
    db: Session = Depends(deps.get_db),
    user_new_info: schemas.UserUpdate,
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """Update one ``user`` entity based on its name.
    """
    return user_web_crud.put_enty_by_name(
        db, name=name, enty_new_info=user_new_info
    )


@users_router.delete(
    '/{name}',
    response_model=schemas.User,
    name='Delete user by name'
)
async def delete_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """Delete one ``user`` entity based on its name.
    """
    return user_web_crud.delete_enty_by_name(db, name=name)
