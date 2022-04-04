from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app import crud, schemas
from app.api import deps

router = APIRouter()


@router("/all", response_model=List[schemas.Device])
def get_all_devices(*, db: Session = Depends(deps.get_db)) -> Any:
    devices = crud.crud_device.get_all(db)

    return devices


@router.get("/", response_model=List[schemas.Device])
def get_devices(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    devices = crud.crud_device.get_multi(db, skip=skip, limit=limit)

    return devices


@router.get("/{id}", response_model=schemas.Device)
def get_device(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    device = crud.crud_device.get(db, id=id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    return device
