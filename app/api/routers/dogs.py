from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app import schemas, crud, models


dogs_router = APIRouter()


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
    all_dogs = {
        'dogs': [
            models.Dog(**dog._asdict()) for dog in crud.dog.get_multi(db)
        ]
    }

    if all_dogs['dogs']:
        return all_dogs
    else:
        raise HTTPException(400, detail='No dogs found')


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
    dog_by_name = crud.dog.get_by_name(db, name_in=name)

    if not dog_by_name:
        raise HTTPException(
            400,
            detail=f'Dog with name \'{name}\' not found.'
        )

    return dog_by_name


@dogs_router.post(
    '/{name}',
    response_model=schemas.Dog,
    name='Save one dog.'
)
async def post_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    dog_info: schemas.DogCreate,
    name: str
) -> Any:
    """Save one ``dog`` entity.
    """
    try:
        created_dog = crud.dog.create(db, obj_in=dog_info)
    except Exception:
        raise HTTPException(
            500,
            detail=f'Error while creating dog \'{name}\' in database.'
        )

    if not created_dog:
        raise HTTPException(
            400,
            detail=f'Create query of dog \'{name}\' finished but was not '
                   'saved.'
        )

    return created_dog


@dogs_router.put(
    '/{name}',
    response_model=schemas.Dog,
    name='Update dog info by name.'
)
async def put_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    dog_new_info: schemas.DogUpdate,
    name: str
) -> Any:
    """Update one ``dog`` entity based on its name.
    """
    try:
        updated_dog = crud.dog.update_by_name(
            db, name_in_db=name, obj_in=dog_new_info
        )
    except Exception:
        raise HTTPException(
            500,
            f'Error while updating dog \'{name}\' in database.'
        )

    if not updated_dog:
        raise HTTPException(
            400,
            f'Dog \'{name}\' was not updated.'
        )

    return updated_dog


@dogs_router.delete(
    '/{name}',
    response_model=schemas.Dog,
    name='Delete dog by name.'
)
async def delete_dogs_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str
) -> Any:
    try:
        deleted_dog = crud.dog.remove_one_by_name(db, name=name)
    except Exception:
        raise HTTPException(
            500,
            f'Error while deleting dog \'{name}\' from database.'
        )

    if not deleted_dog:
        raise HTTPException(
            400,
            f'Dog \'{name}\' was not deleted.'
        )

    return deleted_dog
