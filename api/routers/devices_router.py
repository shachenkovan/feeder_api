from uuid import UUID
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.schemas.devices_schema import DeviceSchemaGet, DeviceSchemaPost, DeviceSchemaUpdate
from database.crud.devices_crud import get_all_devices, get_device_by_id, create_device, update_device, delete_device
from database.db import get_db
from database.models import Devices

device_router = APIRouter(prefix='/device', tags=['Устройства'])


@device_router.get('/all_devices')
def all_devices(db: Session = Depends(get_db)):
    try:
        orm_models = get_all_devices(db)
        result = [DeviceSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@device_router.get('/get_device/{device_id}')
def device_by_id(device_id: UUID, db: Session = Depends(get_db)):
    try:
        orm_model = get_device_by_id(db, device_id)
        result = DeviceSchemaGet.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@device_router.post('/create_device')
def add_device(device: DeviceSchemaPost, db: Session = Depends(get_db)):
    try:
        db_device = Devices(model_id=device.model_id, filial_id=device.filial_id, serial_number=device.serial_number)
        result = create_device(db, db_device)
        return result
    except Exception as e:
        return {"error": str(e)}


@device_router.patch('/update_device/{device_id}')
def update_device_by_id(device_id: UUID, device: DeviceSchemaUpdate, db: Session = Depends(get_db)):
    try:
        data_to_update = device.model_dump(exclude_unset=True)
        return update_device(db, device_id, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@device_router.delete('/delete_device/{device_id}')
def delete_device_by_id(device_id: UUID, db: Session = Depends(get_db)):
    try:
        return delete_device(db, device_id)
    except Exception as e:
        return {"error": str(e)}


