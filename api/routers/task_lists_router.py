from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas.task_lists_schema import TaskListsSchemaGet, TaskListsSchemaPost, TaskListsSchemaUpdate
from authorization.auth import get_current_user
from database.crud.task_lists_crud import get_all_task_lists, get_task_list_by_id, \
    create_task_list, update_task_list, delete_task_list
from database.db import get_db
from database.models import TaskLists

task_list_router = APIRouter(prefix='/task_list')


@task_list_router.get(
    '/all_task_lists',
    response_model=List[TaskListsSchemaGet],
    summary="Получить все списки задач",
    description="Возвращает список всех списков задач в системе."
)
def all_task_lists(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает все списки задач из базы данных.
    Требует авторизации.
    """
    try:
        orm_models = get_all_task_lists(db)
        result = [TaskListsSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списков задач: {str(e)}"
        )


@task_list_router.get(
    '/get_task_list/{task_list_id}',
    response_model=TaskListsSchemaGet,
    summary="Получить список задач по ID",
    description="Возвращает список задач по указанному UUID."
)
def task_list_by_id(
    task_list_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получает конкретный список задач по его UUID.

    Возвращает 404 если список задач не найден.
    """
    try:
        orm_model = get_task_list_by_id(db, task_list_id)
        if not orm_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Список задач с ID {task_list_id} не найден"
            )
        result = TaskListsSchemaGet.model_validate(orm_model)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка задач: {str(e)}"
        )


@task_list_router.post(
    '/create_task_list',
    response_model=TaskListsSchemaGet,
    summary="Создать новый список задач",
    description="Создает новый список задач с указанными параметрами."
)
def add_task_list(
    task_list: TaskListsSchemaPost,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Создает новую запись списка задач.
    """
    try:
        db_task_list = TaskLists(
            device_id=task_list.device_id,
            cmd=task_list.cmd,
            is_regular=task_list.is_regular,
            timing=task_list.timing,
            regular_time_id=task_list.regular_time_id,
            status=task_list.status
        )
        result = create_task_list(db, db_task_list)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании списка задач: {str(e)}"
        )


@task_list_router.patch(
    '/update_task_list/{task_list_id}',
    response_model=TaskListsSchemaGet,
    summary="Обновить список задач",
    description="Обновляет существующий список задач по UUID."
)
def update_task_list_by_id(
    task_list_id: UUID,
    task_list: TaskListsSchemaUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Обновляет поля списка задач.

    Возвращает обновленную запись.

    Возвращает 404, если список задач не найден.
    """
    try:
        data_to_update = task_list.model_dump(exclude_unset=True)
        updated = update_task_list(db, task_list_id, changes=data_to_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Список задач с ID {task_list_id} не найден"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении списка задач: {str(e)}"
        )


@task_list_router.delete(
    '/delete_task_list/{task_list_id}',
    summary="Удалить список задач",
    description="Удаляет список задач по указанному UUID."
)
def delete_task_list_by_id(
    task_list_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаляет список задач по UUID.

    Возвращает подтверждение удаления.

    Возвращает 404, если список задач не найден.
    """
    try:
        deleted = delete_task_list(db, task_list_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Список задач с ID {task_list_id} не найден"
            )
        return {"detail": "Список задач успешно удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении списка задач: {str(e)}"
        )
