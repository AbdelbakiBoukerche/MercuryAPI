from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    fqdn: Optional[str] = None
    serial_number: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    version: Optional[str] = None
    transport: Optional[str] = None

    availability: Optional[bool] = None
    response_time: Optional[int] = None
    sla_availability: Optional[int] = 0
    sla_response_time: Optional[int] = 999

    last_heard: Optional[datetime] = None

    cpu: Optional[int] = None
    memory: Optional[int] = None
    uptime: Optional[int] = None

    os_compliance: Optional[str] = None
    config_compliance: Optional[str] = None
    last_compliance_check: Optional[str] = None

    ssh_port: Optional[int] = None
    ncclient_name: Optional[str] = None
    netconft_port: Optional[int] = None

    hostname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    enable_secret: Optional[str] = None


class DeviceCreate(DeviceBase):
    id: int
    ip_address: str
    name: str
    os: str
    transport: str
    username: str
    hostname: str
    password: str
    enable_secret: str
    ssh_port: int = 22
    vendor: str
    sla_availability: int = 95
    sla_response_time: int = 15


class DeviceUpdate(DeviceBase):
    pass


class Device(DeviceBase):

    class Config:
        orm_mode = True
