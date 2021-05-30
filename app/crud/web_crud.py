from typing import Dict, List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.base_class import Base


class WebCRUDWrapper:
    """Wrapper class to avoid duplicate code in API basic crud operations.
    """
    def __init__(
        self,
        crud: CRUDBase,
        *,
        enty_name: str
    ) -> None:
        self.crud = crud
        self.enty_name: str = enty_name.lower()
        self.enty_name_plural = self.enty_name + 's'

    def get_all_entries(self, db: Session) -> Dict[str, List[Base]]:
        """Get all db entries of entity."""
        all_enties = {
            self.enty_name_plural: [
                self.crud.model(**entity._asdict())
                for entity in self.crud.get_multi(db)
            ]
        }

        if all_enties.get(self.enty_name_plural):
            return all_enties
        else:
            raise HTTPException(
                400,
                detail=f'No {self.enty_name_plural} found'
            )

    def get_enty_by_name(self, db: Session, name: str) -> Base:
        enty_by_name = self.crud.get_by_name(db, name_in=name)

        if not enty_by_name:
            raise HTTPException(
                400,
                detail=f'{self.enty_name.title()} with name \'{name}\' '
                       'not found.'
            )

        return enty_by_name

    def post_enty_by_name(
        self,
        db: Session,
        *,
        name: str,
        enty_info: BaseModel
    ) -> Base:
        try:
            created_enty = self.crud.create(db, obj_in=enty_info)
        except Exception:
            raise HTTPException(
                500,
                detail=f'Error while creating {self.enty_name} \'{name}\' in '
                       'database.'
            )

        if not created_enty:
            raise HTTPException(
                400,
                detail=f'Create query of {self.enty_name} \'{name}\' finished '
                       'but was not saved.'
            )

        return created_enty

    def put_enty_by_name(
        self,
        db: Session,
        *,
        name: str,
        enty_new_info: BaseModel
    ):
        try:
            updated_enty = self.crud.update_by_name(
                db, name_in_db=name, obj_in=enty_new_info
            )
        except Exception:
            raise HTTPException(
                500,
                f'Error while updating {self.enty_name} \'{name}\' in '
                f'database. Probably the {self.enty_name} does not exist in '
                'database.'
            )

        if not updated_enty:
            raise HTTPException(
                400,
                f'{self.enty_name.title()} \'{name}\' was not updated.'
            )

        return updated_enty

    def delete_enty_by_name(
        self,
        db: Session,
        *,
        name: str
    ):
        try:
            deleted_enty = self.crud.remove_one_by_name(db, name=name)
        except Exception:
            raise HTTPException(
                500,
                f'Error while deleting {self.enty_name} \'{name}\' from '
                f'database. Probably the {self.enty_name} does not exist in '
                'database.'
            )

        if not deleted_enty:
            raise HTTPException(
                400,
                f'{self.enty_name.title()} \'{name}\' was not deleted.'
            )

        return deleted_enty
