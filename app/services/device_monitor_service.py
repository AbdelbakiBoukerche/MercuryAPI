from datetime import datetime
import time

import napalm

from app.core.logger import logger
from app.crud.crud_device import crud_device
from app.crud.crud_device_status import crud_device_status
from app.models.device import Device
from app.schemas.device import DeviceUpdate
from app.schemas.device_status import DeviceStatusCreate
from app.utils import get_db


def calculate_cpu(cpu):
    num_cpus = 0
    cpu_total = 0.0
    for cpu, usage in cpu.items():
        cpu_total += usage["%usage"]
        num_cpus += 1
    return int(cpu_total / num_cpus)


def calculate_memory(memory):
    return int((memory["used_ram"] * 100) / memory["available_ram"])


class DeviceMonitorService:
    def __init__(self) -> None:
        self.db = get_db.get_db()
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            logger.debug(f"{self.__class__.__name__}: terminate pending...")

    def monitor(self, interval):

        while True and not self.terminate:

            # Get devices from database
            devices = crud_device.get_all(self.db)
            logger.debug(
                f"{self.__class__.__name__}: started for {len(devices)} devices."
            )

            # For each device:
            for device in devices:

                if device.transport != "napalm":
                    logger.warn(
                        f"{self.__class__.__name__}: skipping {device.name}, only napalm is supported currently!"
                    )
                    continue

                if self.terminate:
                    break

                logger.info(f"{self.__class__.__name__}: started for {device.name}.")

                # Get device facts
                device_status = self.__get_device_status(device=device)
                device_update = DeviceUpdate(
                    availability=device_status["availability"],
                    response_time=device_status["response_time"],
                    cpu=device_status["cpu"],
                    memory=device_status["memory"],
                    last_heard=device_status["last_heard"],
                )

                # Update DeviceStatus and Device in database
                crud_device.update(self.db, db_obj=device, obj_in=device_update)
                device_status_obj = DeviceStatusCreate(
                    availability=device_status["availability"],
                    response_time=device_status["response_time"],
                    cpu=device_status["cpu"],
                    memory=device_status["memory"],
                    device_id=device.id,
                )
                crud_device_status.create(self.db, obj_in=device_status_obj)

            for _ in range(0, int(interval / 10)):
                time.sleep(10)
                if self.terminate:
                    break

        logger.info(f"{self.__class__.__name__}: gracefully exiting...")

    # * Private Methods
    # ! ===============================================================================================================
    def __get_device_status(self, device: Device):
        device_status = dict()
        device_status["availability"] = False
        device_status["response_time"] = None
        device_status["cpu"] = None
        device_status["memory"] = None
        device_status["last_heard"] = None

        env = None
        response_time = None

        if device.os in {"ios", "iosxe", "nxos-ssh"} and device.transport == "napalm":
            try:
                time_start = time.time()
                result, env = self.__get_device_info(device, "environment")
                response_time = time.time() - time_start
            except BaseException as e:
                logger.error(
                    f"{self.__class__.__name__}: Exception when getting environment info for {device.name}!"
                    f"Error: {repr(e)}"
                )
                result = "failed"
        else:

            try:
                time_start = time.time()
                result = env = self.__get_device_info(device, "facts")
                response_time = time.time() - time_start
            except BaseException as e:
                logger.error(
                    f"{self.__class__.__name__}: Exception when getting facts info for {device.name}! Error: {repr(e)}"
                )
                result = "failed"

        if result != "success":
            logger.error(f"{self.__class__.__name__}: {device.name} was not available!")

        else:
            device_status["availability"] = True
            if response_time:
                device_status["response_time"] = int(response_time * 1000)
            device_status["last_heard"] = str(datetime.now())[:-3]

            if env:
                device_status["cpu"] = calculate_cpu(env["environment"]["cpu"])
                device_status["memory"] = calculate_memory(env["environment"]["memory"])

        return device_status

    def __get_device_info(self, device: Device, requested_info, live_info=False):
        if device.transport == "napalm":
            return self.__get_device_info_napalm(device, requested_info, live_info)
        else:
            return "failure", "Unable to retrieve requested info from device"

    def __get_device_info_napalm(self, device: Device, requested_info, live_info=False):
        napalm_device = self.__get_napalm_device(device)

        try:
            napalm_device.open()

            facts = napalm_device.get_facts()
            crud_device.update(self.db, db_obj=device, obj_in=facts)

            if requested_info == "facts":
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

    def __get_napalm_device(self, device: Device):
        if device.os == "ios" or device.os == "iosxe":
            driver = napalm.get_network_driver("ios")
        else:
            return "failed", "Unsupported OS"

        if device.os in {"ios", "iosxe", "nxos-ssh"}:
            napalm_device = driver(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                optional_args={"port": device.ssh_port, "secret": device.enable_secret},
            )
        else:
            napalm_device = driver(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                optional_args={"secret": device.enable_secret},
            )

        return napalm_device
