from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def create(self, db: Session, *, obj_in: DeviceCreate) -> Device:
        return super().create(db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        *,
        db_obj: Device,
        obj_in: Union[DeviceUpdate, Dict[str, Any]]
    ) -> Device:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


crud_device = CRUDDevice(Device)
