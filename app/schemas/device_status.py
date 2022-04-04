from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceStatusBase(BaseModel):
    id: Optional[int] = None

    timestamp: Optional[datetime] = None
    availability: Optional[bool] = None
    response_time: Optional[int] = None
    cpu: Optional[int] = None
    memory: Optional[int] = None

    device_id: Optional[int] = None


class DeviceStatusCreate(DeviceStatusBase):
    timestamp: datetime
    availability: bool
    response_time: int
    cpu: int
    memory: int

    device_id: int


class DeviceStatusUpdate(DeviceStatusBase):
    timestamp: datetime
    availability: bool
    response_time: int
    cpu: int
    memory: int

    device_id: int


class DeviceStatusInDBBase(DeviceStatusBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class DeviceStatus(DeviceStatusInDBBase):
    pass


class DeviceStatusInDB(DeviceStatusInDBBase):
    pass
