from time import sleep

from app.core.logger import logger


class DeviceMonitorService:
    def __init__(self) -> None:
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            logger.debug(
                f"{self.__class__.__name__}: monitor device terminate pending..."
            )

    def monitor(self, interval):
        while True and not self.terminate:
            # Get devices IDs from database
            # For each device:
            # Get device status
            # Update DeviceStatus in database

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        logger.info("Gracefully exiting monitor:device...")
