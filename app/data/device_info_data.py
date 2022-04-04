from enum import Enum

import napalm

from app.core.logger import logger
from app.crud.crud_device import crud_device
from app.db.session import SessionLocal
from app.models.device import Device


class EOperatingSystems(str, Enum):
    IOS = "ios"
    IOSXE = "iosxe"
    NXOS = "nxos"
    NXOS_SSH = "nxos-ssh"


def get_device_info(device: Device, requested_info, get_live_info=False):

    if device.transport == "napalm":
        return get_device_info_napalm(device, requested_info, get_live_info)

    else:
        return "failure", "Unable to retrieve requested info from device"


def get_device_info_napalm(device: Device, requested_info, get_live_info=False):

    # TODO: Use dependency injection for SessoinLocal()
    db = SessionLocal()

    # Try to get the info from the DB first
    if requested_info == "facts" and not get_live_info:
        result, device_info = "success", crud_device.get(db, id=device.id)
        if result == "success":
            return "success", {"device_info": device_info}

    napalm_device = get_napalm_device(device)

    try:
        napalm_device.open()

        if requested_info == "facts":
            facts = napalm_device.get_facts()
            crud_device.update(db, db_obj=device, obj_in=facts)
            return "success", {"facts": facts}
        elif requested_info == "environment":
            return "success", {"environment": napalm_device.get_environment()}
        elif requested_info == "interfaces":
            return "success", {"interfaces": napalm_device.get_interfaces()}
        elif requested_info == "arp":
            return "success", {"arp": napalm_device.get_arp_table()}
        elif requested_info == "mac":
            return "success", {"mac": napalm_device.get_mac_address_table()}
        elif requested_info == "config":
            return "success", {"config": napalm_device.get_config()}
        elif requested_info == "counters":
            return "success", {"counters": napalm_device.get_interfaces_counters()}

        else:
            return "failure", "Unknown requested info"

    except BaseException as e:
        logger.error(
            f"Exception when getting device info for {device.name}! Error: {repr(e)}"
        )
        return "failure", repr(e)


def get_napalm_device(device: Device):

    if device.os == EOperatingSystems.IOS.value or device.os == EOperatingSystems.IOSXE:
        driver = napalm.get_network_driver("ios")
    elif device.os == EOperatingSystems.NXOS_SSH:
        driver = napalm.get_network_driver("nxos_ssh")
    elif device.os == EOperatingSystems.NXOS:
        driver = napalm.get_network_driver("nxos")
    else:
        return "failed", "Unsupported OS"

    if device.os in {
        EOperatingSystems.IOS,
        EOperatingSystems.IOSXE,
        EOperatingSystems.NXOS_SSH,
    }:
        napalm_device = driver(
            hostname=device.ip_address,
            username=device.username,
            password=device.password,
            optional_args={
                "port": device.ssh_port,
                "secret": device.enable_secret,
            },
        )
    else:
        napalm_device = driver(
            hostname=device.ip_address,
            username=device.username,
            password=device.password,
        )

    return napalm_device
