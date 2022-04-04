from typing import Any, Dict, List, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def create(self, db: Session, *, obj_in: DeviceCreate) -> Device:
        db_obj = Device(**obj_in.dict())
        return super().create(db, obj_in=db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: Device,
        obj_in: Union[DeviceUpdate, Dict[str, Any]]
    ) -> Device:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_devices_ids(self, db: Session) -> List[int]:
        devices_ids = db.query(self.model.id).all()
        return [id for id, in devices_ids]


crud_device = CRUDDevice(Device)
