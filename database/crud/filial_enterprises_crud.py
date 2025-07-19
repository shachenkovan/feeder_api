from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from database.models import FilialEnterprises


def create_filial_enterprise(db: Session, filial_enterprise: FilialEnterprises):
    try:
        db.add(filial_enterprise)
        db.commit()
        db.refresh(filial_enterprise)
        return filial_enterprise
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


def get_all_filial_enterprises(db: Session):
    try:
        filial_enterprise = db.query(FilialEnterprises).all()
        filial_enterprise_list = []
        for fil_ent_prise in filial_enterprise:
            filial_enterprise_list.append({'id': fil_ent_prise.id, 'inn': fil_ent_prise.inn,
                                     'adres': fil_ent_prise.adres})
        return filial_enterprise_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_filial_enterprise_by_id(db: Session, filial_enterprise_id: int):
    try:
        if filial_enterprise := db.query(FilialEnterprises).filter(FilialEnterprises.id == filial_enterprise_id).first():
            return filial_enterprise
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_filial_enterprise(db: Session, filial_enterprise_id: int, changes: dict):
    try:
        filial_enterprise = db.query(FilialEnterprises).filter(FilialEnterprises.id == filial_enterprise_id).first()
        if not filial_enterprise:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(filial_enterprise, field):
                setattr(filial_enterprise, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')
        db.commit()
        db.refresh(filial_enterprise)
        return filial_enterprise
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


def delete_filial_enterprise(db: Session, filial_enterprise_id: int):
    try:
        filial_enterprise = db.query(FilialEnterprises).filter(FilialEnterprises.id == filial_enterprise_id).first()
        if not filial_enterprise:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        db.delete(filial_enterprise)
        db.commit()
        return {'msg': f'Удаление записи с id {filial_enterprise_id} прошло успешно.'}
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