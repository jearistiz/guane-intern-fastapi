from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import DogCreate, DogUpdate
from app.models import Dog


class CRUDDog(CRUDBase[Dog, DogCreate, DogUpdate]):
    def get_adopted(
        self, db: Session, *, skip: int = 0, limit: Optional[int] = None
    ) -> List[Dog]:
        return (
            db.query(self.model)
            .filter(self.model.is_adopted == True)  # noqa
            .offset(skip)
            .limit(limit)
            .all()
        )


dog = CRUDDog(Dog)
