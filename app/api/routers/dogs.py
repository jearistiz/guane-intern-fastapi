from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, crud
from app.api import deps
from app.crud import superuser_crud
from app.utils.http_request import get_dog_picture


dogs_router = APIRouter()

# Web crud was implemented as a wrapper to avoid duplicate code between
# the two main routers (dogs, users)
dog_web_crud = crud.WebCRUDWrapper(crud.dog, enty_name='dog')


@dogs_router.get(
    '/',
    response_model=schemas.Dogs,
    name='List of all dogs\' info.'
)
async def get_dogs(
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a list of all ``dog`` entities.
    """
    return dog_web_crud.get_all_entries(db)


@dogs_router.get(
    '/is_adopted',
    response_model=schemas.AdoptedDogs,
    name='Adopted dogs\' info.'
)
async def get_dogs_is_adopted(
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get a list of all ``dog`` entities where the flag ``is_adopted`` is
    True.
    """
    adopted_dogs = crud.dog.get_adopted(db)
    if not adopted_dogs:
        raise HTTPException(
            400,
            detail='No adopted dogs found.'
        )
    return {'adopted_dogs': adopted_dogs}


@dogs_router.get(
    '/{name}',
    response_model=schemas.Dog,
    name='Dog info by name.'
)
async def get_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    """Read one ``dog`` entity based on its name
    """
    return dog_web_crud.get_enty_by_name(db, name)


@dogs_router.post(
    '/{name}',
    response_model=schemas.Dog,
    name='Save one dog.',
    status_code=status.HTTP_201_CREATED,
)
async def post_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    dog_info: schemas.DogCreate,
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """Save one ``dog`` entity. Don't include the field `picture` in your
    request if you want the backend to fill it with a random dog picture URL
    link.
    """
    if dog_info.picture is None:
        dog_info.picture = get_dog_picture()
    return dog_web_crud.post_enty_by_name(db, name=name, enty_info=dog_info)


@dogs_router.put(
    '/{name}',
    response_model=schemas.Dog,
    name='Update dog info by name.',
)
async def put_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    dog_new_info: schemas.DogUpdate,
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """Update one ``dog`` entity based on its name.
    """
    return dog_web_crud.put_enty_by_name(
        db, name=name, enty_new_info=dog_new_info
    )


@dogs_router.delete(
    '/{name}',
    response_model=schemas.Dog,
    name='Delete dog by name.',
)
async def delete_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    return dog_web_crud.delete_enty_by_name(db, name=name)
