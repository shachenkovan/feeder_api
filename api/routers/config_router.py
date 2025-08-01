from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas.config_schema import ConfigSchemaGet, ConfigSchemaPost
from authorization.auth import get_current_user
from database.crud.configs_crud import get_all_settings, set_setting_value, get_setting_by_name
from database.db import get_db

config_router = APIRouter(prefix='/config')


@config_router.get(
    '/get_all_settings',
    response_model=List[ConfigSchemaGet],
    summary="Получить все настройки",
    description="Возвращает список всех конфигурационных параметров системы."
)
def get_all(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Получает все настройки из базы данных.
    Требует авторизации.
    """
    try:
        orm_models = get_all_settings(db)
        result = [ConfigSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении настроек: {str(e)}"
        )


@config_router.get(
    '/get_config/{config_name}',
    response_model=ConfigSchemaGet,
    summary="Получить настройку по имени",
    description="Возвращает конфигурацию по указанному имени параметра."
)
def get_by_name(
        config_name: str,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Получает конкретную настройку по её имени.

    Возвращает 404 если настройка не найдена.
    """
    try:
        setting = get_setting_by_name(db, config_name)
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Настройка '{config_name}' не найдена"
            )
        return setting
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении настройки: {str(e)}"
        )


@config_router.post(
    '/set_setting_value',
    summary="Установить значение настройки",
    description="Создает новую или обновляет существующую настройку."
)
def update_or_add(
        config: ConfigSchemaPost,
        is_force: bool,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Устанавливает значение конфигурационного параметра.

    - is_force=True: создает новую запись, если не найдена для обновления.
    - is_force=False: возвращает ошибку при попытке обновить несуществующую запись.
    """
    try:
        config_update = config.model_dump(exclude_unset=True)
        return set_setting_value(db, config_update['name'], config_update['value'], is_force)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении настройки: {str(e)}"
        )