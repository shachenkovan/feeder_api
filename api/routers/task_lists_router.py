from uuid import UUID
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.schemas.task_lists_schema import TaskListsSchemaGet, TaskListsSchemaPost, TaskListsSchemaUpdate
from authorization.auth import get_current_user
from database.crud.task_lists_crud import get_all_task_lists, get_task_list_by_id, \
    create_task_list, update_task_list, delete_task_list
from database.db import get_db
from database.models import TaskLists

task_list_router = APIRouter(prefix='/task_list', tags=['Список заданий'])


@task_list_router.get('/all_task_lists')
def all_task_lists(db: Session = Depends(get_db),
                   user: dict = Depends(get_current_user)):
    try:
        orm_models = get_all_task_lists(db)
        result = [TaskListsSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@task_list_router.get('/get_task_list/{task_list_id}')
def task_list_by_id(task_list_id: UUID,
                    db: Session = Depends(get_db),
                    user: dict = Depends(get_current_user)):
    try:
        orm_model = get_task_list_by_id(db, task_list_id)
        result = TaskListsSchemaGet.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@task_list_router.post('/create_task_list')
def add_task_list(task_list: TaskListsSchemaPost,
                  db: Session = Depends(get_db),
                  user: dict = Depends(get_current_user)):
    try:
        db_task_list = TaskLists(device_id=task_list.device_id,
                                 cmd=task_list.cmd,
                                 is_regular=task_list.is_regular,
                                 timing=task_list.timing,
                                 regular_time_id=task_list.regular_time_id,
                                 status=task_list.status)
        result = create_task_list(db, db_task_list)
        return result
    except Exception as e:
        return {"error": str(e)}


@task_list_router.patch('/update_task_list/{task_list_id}')
def update_task_list_by_id(task_list_id: UUID,
                           task_list: TaskListsSchemaUpdate,
                           db: Session = Depends(get_db),
                           user: dict = Depends(get_current_user)):
    try:
        data_to_update = task_list.model_dump(exclude_unset=True)
        return update_task_list(db, task_list_id, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@task_list_router.delete('/delete_task_list/{task_list_id}')
def delete_task_list_by_id(task_list_id: UUID,
                           db: Session = Depends(get_db),
                           user: dict = Depends(get_current_user)):
    try:
        return delete_task_list(db, task_list_id)
    except Exception as e:
        return {"error": str(e)}


