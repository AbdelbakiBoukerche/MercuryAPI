from logging import shutdown
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.settings import settings
from app.core.logger import logger
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.services.thread_service import ThreadService


app = FastAPI(
    title=settings.PROJECT_NAME, penapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Init Database
db = SessionLocal()
init_db(db=db)


from app.utils.import_devices import import_devices, EImportDevicesFileType


devices = import_devices(filename="devices.yaml", filetype=EImportDevicesFileType.YAML)


app.include_router(api_router, prefix=settings.API_V1_STR)


ThreadService.start_device_threads(device_monitor_interval=60)


from app.data.device_info_data import get_device_info
from app.models.device import Device

device = Device(**devices[1])
data = get_device_info(device=device, requested_info="facts", get_live_info=True)
print(data)


def shutdown():  # noqa F811
    logger.info("MerucryAPI: Starting shutdown sequence!!!")

    ThreadService.init_terminate_all_threads()

    ThreadService.stop_device_threads()


import atexit

atexit.register(shutdown)
