from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas.devices_schema import DeviceSchemaGet, DeviceSchemaPost, DeviceSchemaUpdate
from authorization.auth import get_current_user
from database.crud.devices_crud import get_all_devices, get_device_by_id, create_device, update_device, delete_device
from database.db import get_db
from database.models import Devices

device_router = APIRouter(prefix='/device')


@device_router.get(
    '/all_devices',
    response_model=List[DeviceSchemaGet],
    summary="Получить все устройства",
    description="Возвращает список всех устройств из базы данных."
)
def all_devices(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает список всех устройств.
    Требует авторизации.
    """
    try:
        orm_models = get_all_devices(db)
        return [DeviceSchemaGet.model_validate(m) for m in orm_models]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении устройств: {str(e)}"
        )


@device_router.get(
    '/get_device/{device_id}',
    response_model=DeviceSchemaGet,
    summary="Получить устройство по ID",
    description="Возвращает устройство по указанному UUID."
)
def device_by_id(
    device_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает устройство по UUID.
    Возвращает 404, если устройство не найдено.
    """
    try:
        orm_model = get_device_by_id(db, device_id)
        if not orm_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Устройство с ID {device_id} не найдено"
            )
        return DeviceSchemaGet.model_validate(orm_model)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении устройства: {str(e)}"
        )


@device_router.post(
    '/create_device',
    response_model=DeviceSchemaGet,
    summary="Создать новое устройство",
    description="Создает новое устройство с указанными параметрами."
)
def add_device(
    device: DeviceSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Создает новое устройство.
    """
    try:
        db_device = Devices(
            model_id=device.model_id,
            filial_id=device.filial_id,
            serial_number=device.serial_number
        )
        created_device = create_device(db, db_device)
        return created_device
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании устройства: {str(e)}"
        )


@device_router.patch(
    '/update_device/{device_id}',
    summary="Обновить устройство",
    description="Обновляет данные устройства по UUID."
)
def update_device_by_id(
    device_id: UUID,
    device: DeviceSchemaUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Обновляет устройство по UUID.
    Возвращает ошибку, если устройство не найдено.
    """
    try:
        data_to_update = device.model_dump(exclude_unset=True)
        updated = update_device(db, device_id, changes=data_to_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Устройство с ID {device_id} не найдено для обновления"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении устройства: {str(e)}"
        )


@device_router.delete(
    '/delete_device/{device_id}',
    summary="Удалить устройство",
    description="Удаляет устройство по UUID."
)
def delete_device_by_id(
    device_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаляет устройство по UUID.
    Возвращает ошибку, если устройство не найдено.
    """
    try:
        deleted = delete_device(db, device_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Устройство с ID {device_id} не найдено для удаления"
            )
        return {"detail": "Устройство успешно удалено"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении устройства: {str(e)}"
        )
