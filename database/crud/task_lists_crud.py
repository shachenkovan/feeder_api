from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.exc import IntegrityError, DataError
from database.models import TaskLists


def create_task_list(db: Session, task_list: TaskLists):
    try:
        db.add(task_list)
        db.commit()
        db.refresh(task_list)
        return task_list
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Не удалось создать, значения в полях должны быть уникальными и не пустыми."
        )
    except DataError:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail="Не удалось создать, неверный тип данных или размер."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_all_task_lists(db: Session):
    try:
        task_lists = db.query(TaskLists).all()
        task_lists_list = []
        for task in task_lists:
            task_lists_list.append({'id': task.id,
                                    'device_id': task.device_id,
                                    'cmd': task.cmd,
                                    'is_regular': task.is_regular,
                                    'timing': task.timing,
                                    'regular_time_id': task.regular_time_id,
                                    'status': task.status})
        return task_lists_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_task_list_by_id(db: Session, task_list_id: UUID):
    try:
        if task_list := db.query(TaskLists).filter(TaskLists.id == str(task_list_id)).first():
            return task_list
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_task_list(db: Session, task_list_id: UUID, changes: dict):
    try:
        task_list = db.query(TaskLists).filter(TaskLists.id == str(task_list_id)).first()
        if not task_list:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(task_list, field):
                setattr(task_list, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')
        db.commit()
        db.refresh(task_list)
        return task_list
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Не удалось создать, значения в полях должны быть уникальными и не пустыми."
        )
    except DataError:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail="Не удалось создать, неверный тип данных или размер."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def delete_task_list(db: Session, task_list_id: UUID):
    try:
        task_list = db.query(TaskLists).filter(TaskLists.id == str(task_list_id)).first()
        if not task_list:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        db.delete(task_list)
        db.commit()
        return {'msg': f'Удаление записи с id {task_list_id} прошло успешно.'}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Не удалось создать, значения в полях должны быть уникальными и не пустыми."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )