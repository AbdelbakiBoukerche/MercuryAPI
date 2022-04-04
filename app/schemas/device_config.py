from datetime import date, datetime
from turtle import st
from typing import Optional

from pydantic import BaseModel


class DeviceConfigBase(BaseModel):
    # id: Optional[int] = None

    timestamp: Optional[datetime] = None
    config: Optional[str] = None

    device_id: Optional[int] = None


class DeviceConfigCreate(DeviceConfigBase):
    timestamp: date
    config: st

    device_id: int


class DeviceConfigUpdate(DeviceConfigBase):
    id: int
    timestamp: date
    config: st

    device_id: int


class DeviceConfig(DeviceConfigBase):
    id: int

    class Config:
        orm_mode = True