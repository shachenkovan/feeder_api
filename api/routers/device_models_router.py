from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas.device_models_schema import DeviceModelSchemaPost, DeviceModelSchemaGet
from authorization.auth import get_current_user
from database.crud.device_models_crud import (
    get_all_device_models,
    create_device_model,
    get_device_model_by_id,
    delete_device_model,
    update_device_model
)
from database.db import get_db
from database.models import DeviceModels

device_model_router = APIRouter(prefix='/device_models')


@device_model_router.get(
    '/all_device_models',
    response_model=List[DeviceModelSchemaGet],
    summary="Получить все модели устройств",
    description="Возвращает список всех моделей устройств из базы данных."
)
def all_device_models(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает список всех моделей устройств.
    Требует авторизации.
    """
    try:
        orm_models = get_all_device_models(db)
        return [DeviceModelSchemaGet.model_validate(m) for m in orm_models]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении моделей устройств: {str(e)}"
        )


@device_model_router.get(
    '/get_device_model/{device_model_id}',
    response_model=DeviceModelSchemaGet,
    summary="Получить модель устройства по ID",
    description="Возвращает модель устройства по заданному ID."
)
def device_model_by_id(
    device_model_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает модель устройства по ID.
    Возвращает 404, если модель не найдена.
    """
    try:
        orm_model = get_device_model_by_id(db, device_model_id)
        if not orm_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Модель устройства с ID {device_model_id} не найдена"
            )
        return DeviceModelSchemaGet.model_validate(orm_model)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении модели устройства: {str(e)}"
        )


@device_model_router.post(
    '/create_device_model',
    response_model=DeviceModelSchemaGet,
    summary="Создать новую модель устройства",
    description="Создает новую модель устройства с указанным именем."
)
def add_device_model(
    device_model: DeviceModelSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Создает новую модель устройства.
    """
    try:
        db_device_model = DeviceModels(name=device_model.name)
        created_model = create_device_model(db, db_device_model)
        return created_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании модели устройства: {str(e)}"
        )


@device_model_router.patch(
    '/update_device_model/{device_model_id}',
    summary="Обновить модель устройства",
    description="Обновляет данные модели устройства по ID."
)
def update_device_model_by_id(
    device_model_id: int,
    device_model: DeviceModelSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Обновляет модель устройства по ID.
    Возвращает ошибку, если обновление не удалось.
    """
    try:
        data_to_update = device_model.model_dump(exclude_unset=True)
        updated = update_device_model(db, device_model_id, changes=data_to_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Модель устройства с ID {device_model_id} не найдена для обновления"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении модели устройства: {str(e)}"
        )


@device_model_router.delete(
    '/delete_device_model/{device_model_id}',
    summary="Удалить модель устройства",
    description="Удаляет модель устройства по ID."
)
def delete_device_model_by_id(
    device_model_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаляет модель устройства по ID.
    Возвращает ошибку, если модель не найдена.
    """
    try:
        deleted = delete_device_model(db, device_model_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Модель устройства с ID {device_model_id} не найдена для удаления"
            )
        return {"detail": "Модель устройства успешно удалена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении модели устройства: {str(e)}"
        )
