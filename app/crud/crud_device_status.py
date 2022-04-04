from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device_status import DeviceStatus
from app.schemas.device_status import DeviceStatusCreate, DeviceStatusUpdate


class CRUDDeviceStatus(CRUDBase[DeviceStatus, DeviceStatusCreate, DeviceStatusUpdate]):
    def create(self, db: Session, *, obj_in: DeviceStatusCreate) -> DeviceStatus:
        db_obj = DeviceStatus(**obj_in.dict())
        return super().create(db, obj_in=db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: DeviceStatus,
        obj_in: Union[DeviceStatusUpdate, Dict[str, Any]]
    ) -> DeviceStatus:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_device_status = CRUDDeviceStatus(DeviceStatus)
