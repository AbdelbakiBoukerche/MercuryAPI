from fastapi import APIRouter

from app.api.api_v1.views import devices


api_router = APIRouter()


api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
