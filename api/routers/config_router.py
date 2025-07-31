from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.schemas.config_schema import ConfigSchemaGet, ConfigSchemaPost
from authorization.auth import get_current_user
from database.crud.configs_crud import get_all_settings, set_setting_value, get_setting_by_name
from database.db import get_db

config_router = APIRouter(prefix='/config', tags=['Конфигурации'])


@config_router.get('/get_all_settings')
def get_all(db: Session = Depends(get_db),
            user: dict = Depends(get_current_user)):
    try:
        orm_models = get_all_settings(db)
        result = [ConfigSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@config_router.get('/get_config/{config_name}')
def get_by_name(config_name: str,
                db: Session = Depends(get_db),
                user: dict = Depends(get_current_user)):
    try:
        return get_setting_by_name(db, config_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении: {str(e)}")


@config_router.post('/set_setting_value')
def update_or_add(config: ConfigSchemaPost,
                  is_force: bool,
                  db: Session = Depends(get_db),
                  user: dict = Depends(get_current_user)):
    try:
        config_update = config.model_dump(exclude_unset=True)
        return set_setting_value(db, config_update['name'], config_update['value'], is_force)
    except Exception as e:
        return {"error": str(e)}