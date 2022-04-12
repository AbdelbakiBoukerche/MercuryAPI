from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceStatusBase(BaseModel):
    # id: Optional[int] = None
    timestamp: Optional[datetime] = None
    availability: Optional[bool] = None
    response_time: Optional[int] = None
    cpu: Optional[int] = None
    memory: Optional[int] = None

    device_id: Optional[int] = None


class DeviceStatusCreate(DeviceStatusBase):
    availability: bool
    device_id: int


class DeviceStatusUpdate(DeviceStatusBase):
    availability: bool
    device_id: int


class DeviceStatus(DeviceStatusBase):
    id: int

    class Config:
        orm_mode = True
