from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from api.schemas.filial_enterprises_schema import (
    FilialEnterprisesSchemaGet,
    FilialEnterprisesSchemaPost,
    FilialEnterprisesSchemaUpdate,
)
from authorization.auth import get_current_user
from database.crud.filial_enterprises_crud import (
    get_all_filial_enterprises,
    get_filial_enterprise_by_id,
    create_filial_enterprise,
    update_filial_enterprise,
    delete_filial_enterprise,
)
from database.db import get_db
from database.models import FilialEnterprises
from typing import List

filial_enterprise_router = APIRouter(prefix='/filial_enterprise')


@filial_enterprise_router.get(
    '/all_filial_enterprises',
    response_model=List[FilialEnterprisesSchemaGet],
    summary="Получить все филиалы предприятий",
    description="Возвращает список всех филиалов предприятий."
)
def all_filial_enterprises(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    try:
        orm_models = get_all_filial_enterprises(db)
        return [FilialEnterprisesSchemaGet.model_validate(m) for m in orm_models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения филиалов: {e}")


@filial_enterprise_router.get(
    '/get_filial_enterprise/{filial_enterprise_id}',
    response_model=FilialEnterprisesSchemaGet,
    summary="Получить филиал предприятия по ID",
    description="Возвращает филиал предприятия по его ID."
)
def filial_enterprise_by_id(
    filial_enterprise_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        orm_model = get_filial_enterprise_by_id(db, filial_enterprise_id)
        if not orm_model:
            raise HTTPException(status_code=404, detail="Филиал предприятия не найден")
        return FilialEnterprisesSchemaGet.model_validate(orm_model)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения филиала: {e}")


@filial_enterprise_router.post(
    '/create_filial_enterprise',
    response_model=FilialEnterprisesSchemaGet,
    summary="Создать филиал предприятия",
    description="Создает новый филиал предприятия."
)
def add_filial_enterprise(
    filial_enterprise: FilialEnterprisesSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        db_filial_enterprise = FilialEnterprises(
            inn=filial_enterprise.inn,
            adres=filial_enterprise.adres,
        )
        result = create_filial_enterprise(db, db_filial_enterprise)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания филиала: {e}")


@filial_enterprise_router.patch(
    '/update_filial_enterprise/{filial_enterprise_id}',
    response_model=FilialEnterprisesSchemaGet,
    summary="Обновить филиал предприятия",
    description="Обновляет данные филиала предприятия по ID."
)
def update_filial_enterprise_by_id(
    filial_enterprise_id: int,
    filial_enterprise: FilialEnterprisesSchemaUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        data_to_update = filial_enterprise.model_dump(exclude_unset=True)
        updated = update_filial_enterprise(db, filial_enterprise_id, changes=data_to_update)
        if not updated:
            raise HTTPException(status_code=404, detail="Филиал предприятия не найден для обновления")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления филиала: {e}")


@filial_enterprise_router.delete(
    '/delete_filial_enterprise/{filial_enterprise_id}',
    summary="Удалить филиал предприятия",
    description="Удаляет филиал предприятия по ID."
)
def delete_filial_enterprise_by_id(
    filial_enterprise_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        deleted = delete_filial_enterprise(db, filial_enterprise_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Филиал предприятия не найден для удаления")
        return {"detail": "Филиал предприятия успешно удалён"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления филиала: {e}")
