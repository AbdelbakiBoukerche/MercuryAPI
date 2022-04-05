from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.device import DeviceBase


class DeviceStatusBase(BaseModel):
    # id: Optional[int] = None
    timestamp: Optional[datetime] = None
    availability: Optional[bool] = None
    response_time: Optional[int] = None
    cpu: Optional[int] = None
    memory: Optional[int] = None

    device_id: Optional[int] = None


class DeviceStatusCreate(DeviceBase):
    availability: bool
    device_id: int


class DeviceStatusUpdate(DeviceBase):
    availability: bool
    device_id: int


class DeviceStatus(DeviceBase):
    id: int

    class Config:
        orm_mode = True
