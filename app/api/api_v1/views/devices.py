from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app import crud, schemas
from app.api.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Device])
def get_devices(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    devices = crud.crud_device.get_multi(db, skip=skip, limit=limit)

    return devices


@router.get("/all", response_model=List[schemas.Device])
def get_all_devices(*, db: Session = Depends(get_db)) -> Any:
    devices = crud.crud_device.get_all(db)

    return devices


@router.get("/test", response_model=List[int])
def test(*, db: Session = Depends(get_db), device: schemas.DeviceCreate) -> Any:
    data = crud.crud_device.get_devices_ids(db)

    return data


@router.get("/{id}", response_model=schemas.Device)
def get_device(*, db: Session = Depends(get_db), id: int) -> Any:
    device = crud.crud_device.get(db, id=id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    return device


@router.get("/{id}/statuses", response_model=List[schemas.DeviceStatus])
def get_device_statuses(
    *, db: Session = Depends(get_db), id: int, skip: int = 0, limit: int = 100
) -> Any:
    print(id)
    device = crud.crud_device.get(db, id=id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    device_statuses = crud.crud_device_status.get_all_by_device_id(
        db, device_id=device.id
    )

    return device_statuses
