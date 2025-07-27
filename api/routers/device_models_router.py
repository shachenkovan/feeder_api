from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.schemas.device_models_schema import DeviceModelSchemaPost, DeviceModelSchemaGet
from autorization.auth import get_current_user
from database.crud.device_models_crud import get_all_device_models, create_device_model, get_device_model_by_id, \
    delete_device_model, update_device_model
from database.db import get_db
from database.models import DeviceModels

device_model_router = APIRouter(prefix='/device_models', tags=['Модели устройств'])


@device_model_router.get('/all_device_models')
def all_device_models(db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    try:
        orm_models = get_all_device_models(db)
        result = [DeviceModelSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@device_model_router.get('/get_device_model/{device_model_id}')
def device_model_by_id(device_model_id: int,
                       db: Session = Depends(get_db),
                       user: dict = Depends(get_current_user)):
    try:
        orm_model = get_device_model_by_id(db, device_model_id)
        result = DeviceModelSchemaGet.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@device_model_router.post('/create_device_model')
def add_device_model(device_model: DeviceModelSchemaPost,
                     db: Session = Depends(get_db),
                     user: dict = Depends(get_current_user)):
    try:
        db_device_model = DeviceModels(name=device_model.name)
        result = create_device_model(db, db_device_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@device_model_router.patch('/update_device_model/{device_model_id}')
def update_device_model_by_id(device_model_id: int,
                              device_model: DeviceModelSchemaPost,
                              db: Session = Depends(get_db),
                              user: dict = Depends(get_current_user)):
    try:
        data_to_update = device_model.model_dump(exclude_unset=True)
        return update_device_model(db, device_model_id, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@device_model_router.delete('/delete_device_model/{device_model_id}')
def delete_device_model_by_id(device_model_id: int,
                              db: Session = Depends(get_db),
                              user: dict = Depends(get_current_user)):
    try:
        return delete_device_model(db, device_model_id)
    except Exception as e:
        return {"error": str(e)}


