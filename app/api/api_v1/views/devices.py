from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Device])
def get_devices(*, db: Session = Depends(deps.get_db)) -> Any:
    devices = crud.crud_device.get_multi(db, skip=0, limit=100)

    return devices
