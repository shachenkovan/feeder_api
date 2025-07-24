import json
import requests
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.crud.configs_crud import set_setting_value, get_setting_by_name
from database.db import get_db
from database.models import Configs


auth_router = APIRouter(tags=['Авторизация'])

WP_TOKEN_URL = 'https://petsfans.ru/wp-json/jwt-auth/v1/token'
WP_USER_INFO_URL = 'https://petsfans.ru/wp-json/wp/v2/users/me'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization")

def get_wp_token(username, password):
    response = requests.post(WP_TOKEN_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("token")
    return None


def get_wp_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(WP_USER_INFO_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


# def update_roles_in_config(db: Session, wp_roles: list):
    # set_setting_value(db, "roles", wp_roles, is_force=True)

# НЕ ПОНИМАЮ ЗАЧЕМ ОБНОВЛЕНИЕ ТАБЛИЦЫ С КОНФИГОМ Т.К. РОЛИ УЖЕ ЕСТЬ
# И НЕТ СПОСОБА ОПРЕДЕЛЯТЬ В КАКУЮ КАТЕГОРИЮ РОЛЕЙ ОПРЕДЕЛЯТЬ НАЗВАНИЕ
# ТО ЕСТЬ Я НИКАК НЕ МОГУ ВЫЯСНИТЬ ЧТО НАПРИМЕР TRANSLATOR ЭТО USER


def get_user_category(db: Session, user_roles: list) -> list:
    categories = set()  # Чтобы не было повторов
    configs = db.query(Configs).filter(Configs.name.ilike('%roles%')).all()

    for role in user_roles:
        for config in configs:
            if role in config.value:
                parts = config.name.split('.')
                if len(parts) >= 3:
                    categories.add(parts[2])  # Добавляем категорию

    return list(categories) if categories else ["unknown"]



def get_current_user(token: str = Depends(oauth2_scheme)):
    user_info = get_wp_user_info(token)
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Неверный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_info


@auth_router.post('/authorization')
async def external_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=400, detail='Неверные логин или пароль.')

    token = get_wp_token(username, password)
    if not token:
        raise HTTPException(status_code=401, detail='Некорректные данные для входа.')

    user_info = get_wp_user_info(token)
    if not user_info:
        raise HTTPException(status_code=500, detail='Не удалось получить данные пользователя.')

    roles = user_info["user"]["roles"]
    # update_roles_in_config(db, roles)
    category = get_user_category(db, roles)

    return {
        "username": user_info.get("name"),
        "wp_id": user_info.get("id"),
        "roles": roles,
        "category": category,
        "access_token": token,
        "token_type": "bearer"
    }

