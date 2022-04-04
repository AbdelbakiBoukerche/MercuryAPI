from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class DeviceConfigBase(BaseModel):
    # id: Optional[int] = None

    timestamp: Optional[datetime] = None
    config: Optional[str] = None

    device_id: Optional[int] = None


class DeviceConfigCreate(DeviceConfigBase):
    timestamp: date
    config: str

    device_id: int


class DeviceConfigUpdate(DeviceConfigBase):
    timestamp: date
    config: str

    device_id: int


class DeviceConfig(DeviceConfigBase):
    id: int

    class Config:
        orm_mode = True
