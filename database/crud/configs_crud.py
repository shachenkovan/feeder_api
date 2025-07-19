from sqlalchemy.orm import Session
from database.models import Configs
from sqlalchemy.exc import IntegrityError, DataError


def set_setting_value(db: Session, name: str, value: str, is_force: bool):
    try:
        config = db.query(Configs).filter(Configs.name == name).first()
        if config:
            config.value = value
        elif is_force:
            config = Configs(name=name, value=value)
            db.add(config)
        else:
            return {'Error': f'Конфигурация с названием {name} не существует.'}
        db.commit()
        if config:
            db.refresh(config)
        return config
    except IntegrityError:
        db.rollback()
        return {'Error': 'Не удалось редактировать, значения должны быть уникальными и не пустыми.'}
    except DataError:
        db.rollback()
        return {'Error': 'Не удалось редактировать, неверный тип данных или размер.'}
    except Exception as e:
        db.rollback()
        return {'Error': f'Непредвиденная ошибка: {str(e)}'}


def get_setting_by_name(db: Session, config_name: str):
    try:
        if config := db.query(Configs).filter(Configs.name == config_name).first():
            return config
        else:
            return {'msg': 'Запись не найдена.'}
    except Exception as e:
        return {'Error': f'Непредвиденная ошибка: {str(e)}'}


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
        return {'Error': f'Непредвиденная ошибка: {str(e)}'}
