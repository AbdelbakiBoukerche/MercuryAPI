from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    # id: Optional[int] = None
    name: str
    # fqdn: Optional[str] = None
    # serial_number: Optional[str] = None
    ip_address: str
    # mac_address: Optional[str] = None
    vendor: str
    # model: Optional[str] = None
    os: str
    # version: Optional[str] = None
    transport: str

    # availability: Optional[bool] = None
    # response_time: Optional[int] = None
    sla_availability: int
    sla_response_time: int

    # last_heard: Optional[datetime] = None

    # cpu: Optional[int] = None
    # memory: Optional[int] = None
    # uptime: Optional[int] = None

    # os_compliance: Optional[bool] = None
    # config_compliance: Optional[bool] = None
    # last_compliance_check: Optional[str] = None

    ssh_port: int
    # ncclient_name: Optional[str] = None
    # netconft_port: Optional[int] = None

    hostname: str
    username: str
    password: str
    enable_secret: str


class DeviceCreate(DeviceBase):
    fqdn: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    ncclient_name: Optional[str] = None
    netconft_port: Optional[int] = None


class DeviceUpdate(DeviceBase):
    fqdn: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    ncclient_name: Optional[str] = None
    netconft_port: Optional[int] = None

    availability: Optional[bool] = None
    response_time: Optional[int] = None

    last_heard: Optional[datetime] = None

    cpu: Optional[int] = None
    memory: Optional[int] = None
    uptime: Optional[int] = None

    os_compliance: Optional[bool] = None
    config_compliance: Optional[bool] = None
    last_compliance_check: Optional[str] = None


class Device(DeviceBase):
    id: int

    fqdn: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    ncclient_name: Optional[str] = None
    netconft_port: Optional[int] = None

    availability: Optional[bool] = None
    response_time: Optional[int] = None

    last_heard: Optional[datetime] = None

    cpu: Optional[int] = None
    memory: Optional[int] = None
    uptime: Optional[int] = None

    os_compliance: Optional[bool] = None
    config_compliance: Optional[bool] = None
    last_compliance_check: Optional[str] = None

    class Config:
        orm_mode = True
