from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


users_router = APIRouter()


@users_router.get(
    '/',
    response_model=schemas.Users,
    name='List all users',
)
async def get_users(
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get a list of all ``user`` entities.
    """
    all_users = {
        'users': [
            models.User(**user._asdict()) for user in crud.user.get_multi(db)
        ]
    }

    if all_users.get('users'):
        return all_users
    else:
        raise HTTPException(400, detail='No users found')


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
    user_by_name = crud.user.get_by_name(db, name_in=name)

    if not user_by_name:
        raise HTTPException(
            400,
            detail=f'User with name \'{name}\' not found.'
        )

    return user_by_name


@users_router.post(
    '/{name}',
    response_model=schemas.User,
    name='Save user'
)
async def post_users_name(
    *,
    db: Session = Depends(deps.get_db),
    user_info: schemas.UserCreate,
    name: str
) -> Any:
    """Save one ``user`` entity.
    """
    try:
        created_user = crud.user.create(db, obj_in=user_info)
    except Exception:
        raise HTTPException(
            500,
            detail=f'Error while creating user \'{name}\' in database.'
        )

    if not created_user:
        raise HTTPException(
            400,
            detail=f'Create query of user \'{name}\' finished but was not '
                   'saved.'
        )

    return created_user


@users_router.put(
    '/{name}',
    response_model=schemas.User,
    name='Update user by name'
)
async def put_users_name(
    *,
    db: Session = Depends(deps.get_db),
    user_new_info: schemas.UserUpdate,
    name: str
) -> Any:
    """Update one ``user`` entity based on its name.
    """
    try:
        updated_user = crud.user.update_by_name(
            db, name_in_db=name, obj_in=user_new_info
        )
    except Exception:
        raise HTTPException(
            500,
            f'Error while updating user \'{name}\' in database. '
            'Probably the user does not exist in database.'
        )

    if not updated_user:
        raise HTTPException(
            400,
            f'User \'{name}\' was not updated.'
        )

    return updated_user


@users_router.delete(
    '/{name}',
    response_model=schemas.User,
    name='Delete user by name'
)
async def delete_users_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Delete one ``user`` entity based on its name.
    """
    try:
        deleted_user = crud.user.remove_one_by_name(db, name=name)
    except Exception:
        raise HTTPException(
            500,
            f'Error while deleting user \'{name}\' from database. '
            'Probably the user does not exist in database.'
        )

    if not deleted_user:
        raise HTTPException(
            400,
            f'User \'{name}\' was not deleted.'
        )

    return deleted_user
