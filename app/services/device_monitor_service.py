from time import sleep

from app.db.session import SessionLocal
from app.core.logger import logger
from app.crud.crud_device import crud_device


class DeviceMonitorService:
    def __init__(self) -> None:
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            logger.debug(f"{self.__class__.__name__}: terminate pending...")

    def monitor(self, interval):
        # TODO: Use dependency injection for SessoinLocal()
        db = SessionLocal()

        while True and not self.terminate:

            # Get devices from database
            devices = crud_device.get_all(db)
            logger.info(f"{self.__class__.__name__}: started for {len(devices)} devices.")

            # For each device:
            for device in devices:

                # Get device status
                if device.transport != "napalm":
                    logger.warn(
                        f"{self.__class__.__name__}: skipping {device.name}, only napalm is supported currently!")
                    continue

                if self.terminate:
                    break

                logger.info(f"{self.__class__.__name__}: started for {device.name}.")

                # Update DeviceStatus in database

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        logger.info(f"{self.__class__.__name__}: gracefully exiting...")
