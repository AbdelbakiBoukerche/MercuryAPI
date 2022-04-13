from logging import shutdown
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.settings import settings
from app.core.logger import logger
from app.db.init_db import init_db
from app.services.thread_service import ThreadService
from app.utils.get_db import get_db


app = FastAPI(
    title=settings.PROJECT_NAME, penapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    pass
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Init Database
db = get_db()
init_db(db=db)


from app.utils.import_devices import import_devices, EImportDevicesFileType


import_devices(filename="devices.yaml", filetype=EImportDevicesFileType.YAML)


app.include_router(api_router, prefix=settings.API_V1_STR)


# ThreadService.start_device_threads(
#     device_monitor_interval=settings.MONITORING_DEVICE_INTERVAL
# )


if settings.DB_CLEANUP_INTERVAL:
    print("clean database is ON")


def shutdown():  # noqa F811
    logger.info("MerucryAPI: Starting shutdown sequence!!!")

    ThreadService.init_terminate_all_threads()

    ThreadService.stop_device_threads()


import atexit

atexit.register(shutdown)
