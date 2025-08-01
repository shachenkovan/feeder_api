from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas.regular_times_schema import RegularTimesSchemaGet, RegularTimesSchemaPost, RegularTimesSchemaUpdate
from authorization.auth import get_current_user
from database.crud.regular_times_crud import get_all_regular_times, get_regular_time_by_id, \
    create_regular_time, update_regular_time, delete_regular_time
from database.db import get_db
from database.models import RegularTimes

regular_time_router = APIRouter(prefix='/regular_time')


@regular_time_router.get(
    '/all_regular_times',
    response_model=List[RegularTimesSchemaGet],
    summary="Получить все регулярные времена",
    description="Возвращает список всех записей регулярного времени."
)
def all_regular_times(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает все записи регулярного времени из базы данных.
    Требует авторизации.
    """
    try:
        orm_models = get_all_regular_times(db)
        result = [RegularTimesSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении записей: {str(e)}"
        )


@regular_time_router.get(
    '/get_regular_time/{regular_time_id}',
    response_model=RegularTimesSchemaGet,
    summary="Получить запись регулярного времени по ID",
    description="Возвращает запись регулярного времени по указанному идентификатору."
)
def regular_time_by_id(
    regular_time_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает запись регулярного времени по её идентификатору.

    Возвращает 404 если запись не найдена.
    """
    try:
        orm_model = get_regular_time_by_id(db, regular_time_id)
        if not orm_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {regular_time_id} не найдена"
            )
        result = RegularTimesSchemaGet.model_validate(orm_model)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении записи: {str(e)}"
        )


@regular_time_router.post(
    '/create_regular_time',
    response_model=RegularTimesSchemaGet,
    summary="Создать новую запись регулярного времени",
    description="Создает новую запись регулярного времени с указанными параметрами."
)
def add_regular_time(
    regular_time: RegularTimesSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Создает новую запись регулярного времени.
    """
    try:
        db_regular_time = RegularTimes(
            period=regular_time.period,
            days=regular_time.days,
            timing=regular_time.timing
        )
        result = create_regular_time(db, db_regular_time)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании записи: {str(e)}"
        )


@regular_time_router.patch(
    '/update_regular_time/{regular_time_id}',
    response_model=RegularTimesSchemaGet,
    summary="Обновить запись регулярного времени",
    description="Обновляет существующую запись регулярного времени по идентификатору."
)
def update_regular_time_by_id(
    regular_time_id: int,
    regular_time: RegularTimesSchemaUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Обновляет поля записи регулярного времени.

    Возвращает обновленную запись.
    """
    try:
        data_to_update = regular_time.model_dump(exclude_unset=True)
        updated = update_regular_time(db, regular_time_id, changes=data_to_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {regular_time_id} не найдена"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении записи: {str(e)}"
        )


@regular_time_router.delete(
    '/delete_regular_time/{regular_time_id}',
    summary="Удалить запись регулярного времени",
    description="Удаляет запись регулярного времени по идентификатору."
)
def delete_regular_time_by_id(
    regular_time_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаляет запись регулярного времени по ID.

    Возвращает подтверждение удаления.
    """
    try:
        deleted = delete_regular_time(db, regular_time_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {regular_time_id} не найдена"
            )
        return {"detail": "Запись успешно удалена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении записи: {str(e)}"
        )
