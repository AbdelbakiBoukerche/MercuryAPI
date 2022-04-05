from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def create(self, db: Session, *, obj_in: DeviceCreate) -> Device:
        db_obj = Device(
            id=obj_in.id,
            ip_address=obj_in.ip_address,
            name=obj_in.name,
            os=obj_in.os,
            transport=obj_in.transport,
            hostname=obj_in.hostname,
            username=obj_in.username,
            password=obj_in.password,
            enable_secret=obj_in.enable_secret,
            ssh_port=obj_in.ssh_port,
            vendor=obj_in.vendor,
            sla_availability=obj_in.sla_availability,
            sla_response_time=obj_in.sla_response_time,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Device,
        obj_in: Union[DeviceUpdate, Dict[str, Any]]
    ) -> DeviceUpdate:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_device = CRUDDevice(Device)
