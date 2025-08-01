from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from authorization.auth import get_current_user
from database.crud.enterprices_crud import get_enterprise_by_inn, get_all_enterprises, create_enterprise, \
    update_enterprise, delete_enterprise
from api.schemas.enterprices_schema import EnterprisesSchema, EnterprisesSchemaUpdate
from database.db import get_db
from database.models import Enterprises
from typing import List

enterprise_router = APIRouter(prefix='/enterprise')


@enterprise_router.get(
    '/all_enterprises',
    response_model=List[EnterprisesSchema],
    summary="Получить все предприятия",
    description="Возвращает список всех предприятий из базы данных."
)
def all_enterprises(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Получение списка всех предприятий.
    Требуется авторизация.
    """
    try:
        orm_models = get_all_enterprises(db)
        result = [EnterprisesSchema.model_validate(m) for m in orm_models]
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении предприятий: {str(e)}"
        )


@enterprise_router.get(
    '/get_enterprise/{enterprise_inn}',
    response_model=EnterprisesSchema,
    summary="Получить предприятие по ИНН",
    description="Возвращает предприятие по его ИНН. Возвращает 404, если не найдено."
)
def enterprise_by_inn(
        enterprise_inn: str,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Получение предприятия по ИНН.
    """
    try:
        orm_model = get_enterprise_by_inn(db, enterprise_inn)
        if not orm_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Предприятие с ИНН '{enterprise_inn}' не найдено"
            )
        result = EnterprisesSchema.model_validate(orm_model)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении предприятия: {str(e)}"
        )


@enterprise_router.post(
    '/create_enterprise',
    response_model=EnterprisesSchema,
    summary="Создать новое предприятие",
    description="Создает новое предприятие в базе данных."
)
def add_enterprise(
        enterprise: EnterprisesSchema,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Создание нового предприятия.
    """
    try:
        db_enterprise = Enterprises(
            inn=enterprise.inn,
            ogrn=enterprise.ogrn,
            kpp=enterprise.kpp,
            name=enterprise.name,
            adres=enterprise.adres
        )
        result = create_enterprise(db, db_enterprise)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании предприятия: {str(e)}"
        )


@enterprise_router.patch(
    '/update_enterprise/{enterprise_inn}',
    response_model=EnterprisesSchema,
    summary="Обновить данные предприятия",
    description="Обновляет существующее предприятие по ИНН."
)
def update_enterprise_by_inn(
        enterprise_inn: str,
        enterprise: EnterprisesSchemaUpdate,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Обновление данных предприятия по ИНН.
    """
    try:
        data_to_update = enterprise.model_dump(exclude_unset=True)
        updated = update_enterprise(db, enterprise_inn, changes=data_to_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Предприятие с ИНН '{enterprise_inn}' не найдено для обновления"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении предприятия: {str(e)}"
        )


@enterprise_router.delete(
    '/delete_enterprise/{enterprise_inn}',
    summary="Удалить предприятие",
    description="Удаляет предприятие по ИНН."
)
def delete_enterprise_by_inn(
        enterprise_inn: str,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    """
    Удаление предприятия по ИНН.
    """
    try:
        deleted = delete_enterprise(db, enterprise_inn)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Предприятие с ИНН '{enterprise_inn}' не найдено для удаления"
            )
        return {"detail": "Предприятие успешно удалено"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении предприятия: {str(e)}"
        )
