from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Configs
from sqlalchemy.exc import IntegrityError, DataError


def set_setting_value(db: Session, name: str, value: dict, is_force: bool):
    try:
        config = db.query(Configs).filter(Configs.name == name).first()
        if config:
            current_values = config.value or []
            updated_values = list(set(current_values) | set(value))
            config.value = updated_values
        else:
            if is_force:
                config = Configs(name=name, value=value)
                db.add(config)
            else:
                raise HTTPException(status_code=422, detail=f'Конфигурация с названием {name} не существует.')
        db.commit()
        if config:
            db.refresh(config)
        return config
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


def get_setting_by_name(db: Session, config_name: str):
    try:
        if config := db.query(Configs).filter(Configs.name == config_name).first():
            return config
        else:
            raise HTTPException(status_code=404, detail='Запись не найдена.')
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )

def get_all_settings(db: Session):
    try:
        configs = db.query(Configs).all()
        configs_list = []
        for config in configs:
            configs_list.append({'id': config.id,
                                'name': config.name,
                                'value': config.value})
        return configs_list
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )
