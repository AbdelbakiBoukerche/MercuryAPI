from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device_status import DeviceStatus
from app.schemas.device_status import DeviceStatusCreate, DeviceStatusUpdate


class CRUDDeviceStatus(CRUDBase[DeviceStatus, DeviceStatusCreate, DeviceStatusUpdate]):
    def create(self, db: Session, *, obj_in: DeviceStatusCreate) -> DeviceStatus:
        return super().create(db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        *,
        db_obj: DeviceStatus,
        obj_in: Union[DeviceStatusUpdate, Dict[str, Any]]
    ) -> DeviceStatus:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


crud_device_status = CRUDDeviceStatus(DeviceStatus)
