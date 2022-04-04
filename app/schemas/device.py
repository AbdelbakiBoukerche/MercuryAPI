from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    id: int
    name: str
    fqdn: Optional[str] = None
    serial_number: Optional[str] = None
    ip_address: str
    mac_address: Optional[str] = None
    vendor: str
    model: Optional[str] = None
    os: str
    version: Optional[str] = None
    transport: str

    availability: Optional[bool] = None
    response_time: Optional[int] = None
    sla_availability: int
    sla_response_time: int

    last_heard: Optional[datetime] = None

    cpu: Optional[int] = None
    memory: Optional[int] = None
    uptime: Optional[int] = None

    os_compliance: Optional[bool] = None
    config_compliance: Optional[bool] = None
    last_compliance_check: Optional[str] = None

    ssh_port: int
    ncclient_name: Optional[str] = None
    netconft_port: Optional[int] = None

    hostname: str
    username: str
    password: str


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class Device(DeviceBase):
    class Config:
        orm_mode = True
