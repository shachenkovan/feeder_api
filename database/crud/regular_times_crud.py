from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError
from database.models import RegularTimes


def create_regular_time(db: Session, regular_time: RegularTimes):
    try:
        db.add(regular_time)
        db.commit()
        db.refresh(regular_time)
        return regular_time
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


def get_all_regular_times(db: Session):
    try:
        regular_times = db.query(RegularTimes).all()
        regular_times_list = []
        for time in regular_times:
            regular_times_list.append({'id': time.id,
                                    'period': time.period,
                                    'days': time.days,
                                    'timing': time.timing})
        return regular_times_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_regular_time_by_id(db: Session, regular_time_id: int):
    try:
        if regular_time := db.query(RegularTimes).filter(RegularTimes.id == regular_time_id).first():
            return regular_time
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_regular_time(db: Session, regular_time_id: int, changes: dict):
    try:
        regular_time = db.query(RegularTimes).filter(RegularTimes.id == regular_time_id).first()
        if not regular_time:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(regular_time, field):
                setattr(regular_time, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')
        db.commit()
        db.refresh(regular_time)
        return regular_time
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


def delete_regular_time(db: Session, regular_time_id: int):
    try:
        regular_time = db.query(RegularTimes).filter(RegularTimes.id == regular_time_id).first()
        if not regular_time:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        db.delete(regular_time)
        db.commit()
        return {'msg': f'Удаление записи с id {regular_time_id} прошло успешно.'}
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