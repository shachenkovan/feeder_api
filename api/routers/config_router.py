from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.schemas.config_schema import ConfigSchemaGet, ConfigSchemaPost
from database.crud.configs_crud import get_all_settings, get_setting_by_name, set_setting_value
from database.db import get_db
from database.models import Configs

config_router = APIRouter(prefix='/config', tags=['Конфигурации'])


@config_router.get('/get_all_settings')
def get_all(db: Session = Depends(get_db)):
    try:
        orm_models = get_all_settings(db)
        result = [ConfigSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@config_router.get('/get_config/{config_id}')
def get_by_name(config_name: str, db: Session = Depends(get_db)):
    try:
        config = db.query(Configs).filter(Configs.name == config_name).first()
        if not config:
            raise HTTPException(status_code=404, detail='Запись не найдена.')
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении: {str(e)}")


@config_router.post('/set_setting_value')
def update_or_add(config: ConfigSchemaPost, is_force: bool, db: Session = Depends(get_db)):
    try:
        config_update = config.model_dump(exclude_unset=True)
        return set_setting_value(db, config_update['name'], config_update['value'], is_force)
    except Exception as e:
        return {"error": str(e)}