from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Enterprises
from sqlalchemy.exc import IntegrityError, DataError


def create_enterprise(db: Session, enterprise: Enterprises):
    try:
        db.add(enterprise)
        db.commit()
        db.refresh(enterprise)
        return enterprise
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


def get_all_enterprises(db: Session):
    try:
        enterprises = db.query(Enterprises).all()
        enterprises_list = []
        for ent_prise in enterprises:
            enterprises_list.append({'inn': ent_prise.inn, 'ogrn': ent_prise.ogrn,
                                     'kpp': ent_prise.kpp,
                                     'name': ent_prise.name,
                                     'adres': ent_prise.adres})
        return enterprises_list
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def get_enterprise_by_inn(db: Session, enterprise_inn: str):
    try:
        enterprise = db.query(Enterprises).filter(Enterprises.inn == enterprise_inn).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail="Запись не найдена.")
        else:
            return enterprise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )


def update_enterprise(db: Session, enterprise_inn: str, changes: dict):
    try:
        enterprise = db.query(Enterprises).filter(Enterprises.inn == enterprise_inn).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail="Запись не найдена.")

        for field, value in changes.items():
            if hasattr(enterprise, field):
                setattr(enterprise, field, value)
            else:
                db.rollback()
                raise HTTPException(status_code=422, detail=f'Поле "{field}" не существует в модели.')
        db.commit()
        db.refresh(enterprise)
        return enterprise
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


def delete_enterprise(db: Session, enterprise_inn: str):
    try:
        enterprise = db.query(Enterprises).filter(Enterprises.inn == enterprise_inn).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail='Запись для удаления не найдена.')
        db.delete(enterprise)
        db.commit()
        return {"msg": f'Удаление записи с inn {enterprise_inn} прошло успешно.'}
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