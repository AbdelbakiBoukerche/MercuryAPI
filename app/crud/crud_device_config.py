from typing import Any, Dict, Union

from sqlalchemy.orm import Session


from app.crud.base import CRUDBase
from app.models.device_config import DeviceConfig
from app.schemas.device_config import DeviceConfigCreate, DeviceConfigUpdate


class CRUDDeviceConfig(CRUDBase[DeviceConfig, DeviceConfigCreate, DeviceConfigUpdate]):
    def create(self, db: Session, *, obj_in: DeviceConfigCreate) -> DeviceConfig:
        db_obj = DeviceConfig(**obj_in.dict())
        return super().create(db, obj_in=db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: DeviceConfig,
        obj_in: Union[DeviceConfigUpdate, Dict[str, Any]]
    ) -> DeviceConfig:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_device_config = CRUDDeviceConfig(DeviceConfig)
