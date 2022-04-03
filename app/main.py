from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings

from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.api.api_v1.api import api_router


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


import_devices(filename="devices.yaml", filetype=EImportDevicesFileType.YAML)


app.include_router(api_router, prefix=settings.API_V1_STR)
