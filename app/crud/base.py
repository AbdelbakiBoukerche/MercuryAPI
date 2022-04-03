from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """CRUD Object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            `model (Type[ModelType])`: SQLAlchemy Model Class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get Object by ID

        Args:
            `db (Session)`: sqlalchemy.orm.Session Instance
            `id (Any)`: ID Of object to query

        Returns:
            `Optional[ModelType]`: Model Instance
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get List of Objects

        Args:
            `db (Session)`: sqlalchemy.orm.Session Instance
            `skip (int, optional)`: Query offset. Defaults to 0.
            `limit (int, optional)`: Query limit from offest. Defaults to 100.

        Returns:
            `List[ModelType]`: List of Model Instance
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Creates item in database from `obj_in`

        Args:
            `db (Session)`: sqlalchemy.orm.Session Instance
            `obj_in (CreateSchemaType)`: Pydantic CreateSchema for the object

        Returns:
            `ModelType`: Model Instance
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Updates the item in the database from `obj_In`

        Args:
            `db (Session)`: sqlalchemy.orm.Session Instance
            `db_obj (ModelType)`: Model Instance of the item to update
            `obj_in (Union[UpdateSchemaType, Dict[str, Any]])`: Pydantic UpdateSchema for the object or Dictionary

        Returns:
            `ModelType`: _description_
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Removes the item with `id` if found

        Args:
            `db (Session)`: sqlalchemy.orm.Session Instance
            `id (int)`: ID of item to remove

        Returns:
            `ModelType`: is None if Item was removed
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()

        return obj
