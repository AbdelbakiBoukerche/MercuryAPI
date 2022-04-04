import threading

from app.core.logger import logger

from .device_monitor_service import DeviceMonitorService


class ThreadService:

    device_monitor_service: DeviceMonitorService = None
    device_monitor_thread: threading.Thread = None

    @staticmethod
    def stop_device_threads():
        logger.info("ThreadService: stopping device monitoring threads...")

        if ThreadService.device_monitor_service and ThreadService.device_monitor_thread:
            ThreadService.device_monitor_service.set_terminate()
            ThreadService.device_monitor_thread.join()

        ThreadService.device_monitor_service = None
        ThreadService.device_monitor_thread = None

    @staticmethod
    def start_device_threads(device_monitor_interval: int = 60):
        ThreadService.device_monitor_service = DeviceMonitorService()
        ThreadService.device_monitor_thread = threading.Thread(
            target=ThreadService.device_monitor_service.monitor,
            args=(device_monitor_interval,),
        )
        ThreadService.device_monitor_thread.start()

    @staticmethod
    def init_terminate_all_threads():
        if ThreadService.device_monitor_service and ThreadService.device_monitor_thread:
            ThreadService.device_monitor_service.set_terminate()
