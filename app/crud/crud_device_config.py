from typing import Any, Dict, Union

from sqlalchemy.orm import Session


from app.crud.base import CRUDBase
from app.models.device_config import DeviceConfig
from app.schemas.device_config import DeviceConfigCreate, DeviceConfigUpdate


class CRUDDeviceConfig(CRUDBase[DeviceConfig, DeviceConfigCreate, DeviceConfigUpdate]):
    def create(self, db: Session, *, obj_in: DeviceConfigCreate) -> DeviceConfig:
        return super().create(db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        *,
        db_obj: DeviceConfig,
        obj_in: Union[DeviceConfigUpdate, Dict[str, Any]]
    ) -> DeviceConfig:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


crud_device_config = CRUDDeviceConfig(DeviceConfig)
