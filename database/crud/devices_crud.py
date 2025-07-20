from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from database.models import Devices


def create_device(db: Session, device: Devices):
    try:
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
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


def get_all_devices(db: Session):
    try:
        devices = db.query(Devices).all()
        devices_list = []
        for dev in devices:
            devices_list.append({'id': dev.id, 'model_id': dev.model_id, 'serial_number': dev.serial_number, 'filial_id': dev.filial_id})
        return devices_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_device_by_id(db: Session, device_id: UUID):
    try:
        if device := db.query(Devices).filter(Devices.id == str(device_id)).first():
            return device
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_device(db: Session, device_id: UUID, changes: dict):
    try:
        device = db.query(Devices).filter(Devices.id == str(device_id)).first()
        if not device:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(device, field):
                setattr(device, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')
        db.commit()
        db.refresh(device)
        return device
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


def delete_device(db: Session, device_id: UUID):
    try:
        device = db.query(Devices).filter(Devices.id == str(device_id)).first()
        if not device:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        db.delete(device)
        db.commit()
        return {'msg': f'Удаление записи с id {device_id} прошло успешно.'}
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