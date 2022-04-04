from enum import Enum
import json
import yaml

from app.core.logger import logger
from app.crud.crud_device import crud_device
from app.db.session import SessionLocal
from app.schemas.device import DeviceCreate


class EImportDevicesFileType(Enum):
    JSON = 0
    YAML = 1


def set_device(devices):
    db = SessionLocal()

    ids = set()
    names = set()

    # Get Devices in database
    devices_in_db = crud_device.get_all(db)

    # Register Existing devices
    for device_in_db in devices_in_db:
        ids.add(device_in_db.id)
        names.add(device_in_db.name)

    # Regiseter new devices
    for device in devices:
        if device["id"] in ids:
            logger.warn(
                f"Error importing devices from devices.yaml! Duplicate device id: {device['id']}"
            )
            continue
        if device["name"] in ids:
            logger.warn(
                f"Error importing devices from devices.yaml! Duplicate device name: {device['name']}"
            )
            continue

        ids.add(device["id"])
        names.add(device["name"])

        device_obj = DeviceCreate(**device)

        crud_device.create(db, obj_in=device_obj)


def import_devices(
    filename: str = None, filetype: EImportDevicesFileType = None
) -> dict:
    if not filename or not filetype:
        return None

    with open(f"app/mock/{filename}", "r") as imported_file:

        if filetype == EImportDevicesFileType.JSON:
            devices = json.loads(imported_file.read())
        if filetype == EImportDevicesFileType.YAML:
            devices = yaml.safe_load(imported_file.read())

    set_device(devices)
    return devices
