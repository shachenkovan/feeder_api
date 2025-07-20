from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError, NoResultFound
from sqlalchemy.orm import Session
from database.models.device_models_model import DeviceModels


def create_device_model(db: Session, device_model: DeviceModels):
    try:
        db.add(device_model)
        db.commit()
        db.refresh(device_model)
        return device_model
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


def get_all_device_models(db: Session):
    try:
        device_models = db.query(DeviceModels).all()
        device_models_list = []
        for models in device_models:
            device_models_list.append({'id': models.id, 'name': models.name})
        return device_models_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_device_model_by_id(db: Session, device_model_id: int):
    try:
        if device_model := db.query(DeviceModels).filter(DeviceModels.id == device_model_id).first():
            return device_model
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_device_model(db: Session, device_model_id: int, changes: dict):
    try:
        device_model = db.query(DeviceModels).filter(DeviceModels.id == device_model_id).first()
        if not device_model:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(device_model, field):
                setattr(device_model, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')

        db.commit()
        db.refresh(device_model)
        return device_model
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


def delete_device_model(db: Session, device_model_id: int):
    try:
        device_model = db.query(DeviceModels).filter(DeviceModels.id == device_model_id).first()
        if not device_model:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        db.delete(device_model)
        db.commit()
        return {'msg': f'Удаление записи с id {device_model_id} прошло успешно.'}
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
