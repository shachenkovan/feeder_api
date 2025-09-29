import secrets

from jose import jwt
from datetime import datetime, timedelta
import requests
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import config
from database.crud.configs_crud import set_setting_value, get_setting_by_name
from database.db import get_db
from database.models import Configs

auth_router = APIRouter()

WP_TOKEN_URL = 'https://petsfans.ru/wp-json/jwt-auth/v1/token'
WP_USER_INFO_URL = 'https://petsfans.ru/wp-json/wp/v2/users/me'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization_local")


def get_wp_token(username: str, password: str) -> Optional[str]:
    """
    Получить JWT токен WordPress через API.
    """
    response = requests.post(WP_TOKEN_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("token")
    return None


def get_wp_user_info(token: str) -> Optional[dict]:
    """
    Получить информацию о пользователе из WordPress API по JWT токену.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(WP_USER_INFO_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def get_local_user_info(token: str) -> Optional[dict]:
    """
    Получить информацию о пользователе по локальному токену.
    """
    # Проверяем, что токен начинается с "local-token-"
    if not token.startswith("local-token-"):
        return None

    try:
        # Извлекаем username из токена: local-token-USERNAME-hexcode
        parts = token.split("-")
        if len(parts) >= 3:
            username = parts[2]

            # Проверяем, существует ли пользователь
            if username in local_users_db:
                user_data = local_users_db[username]
                return {
                    "name": user_data["name"],
                    "id": user_data["id"],
                    "user": {
                        "roles": user_data["roles"]
                    }
                }
    except (IndexError, KeyError, AttributeError):
        pass

    return None


test_wp_roles_dict = {
    "admins": ["administrator"],
    "moders": ["editor"],
    "users": ["subscriber", "contributor", "author", "translator"]
}


def update_roles_in_config(db: Session, wp_roles: dict):
    """
    Синхронизировать роли из WordPress с настройками в базе данных.
    Если роли отличаются - обновить в конфигурации.
    """
    admins_roles_in_wp = wp_roles["admins"]
    admins_roles_list = db.query(Configs).filter(Configs.name.ilike('%administrator%')).first()
    admin_roles_in_db = admins_roles_list.value if admins_roles_list else []
    if sorted(admin_roles_in_db) != sorted(admins_roles_in_wp):
        set_setting_value(db, 'system.roles.administrator', admins_roles_in_wp, is_force=True)

    moder_roles_in_wp = wp_roles["moders"]
    moders_roles_list = db.query(Configs).filter(Configs.name.ilike('%moderator%')).first()
    moder_roles_in_db = moders_roles_list.value if moders_roles_list else []
    if sorted(moder_roles_in_db) != sorted(moder_roles_in_wp):
        set_setting_value(db, 'system.roles.moderator', moder_roles_in_wp, is_force=True)

    user_roles_in_wp = wp_roles["users"]
    users_roles_list = db.query(Configs).filter(Configs.name.ilike('%user%')).first()
    user_roles_in_db = users_roles_list.value if users_roles_list else []
    if sorted(user_roles_in_db) != sorted(user_roles_in_wp):
        set_setting_value(db, 'system.roles.user', user_roles_in_wp, is_force=True)


def get_user_category(db: Session, user_roles: List[str]) -> List[str]:
    """
    Определить категорию пользователя на основе его ролей и конфигурации в БД.
    """
    categories = set()
    configs = db.query(Configs).filter(Configs.name.ilike('%roles%')).all()

    for role in user_roles:
        for config in configs:
            if role in config.value:
                parts = config.name.split('.')
                if len(parts) >= 3:
                    categories.add(parts[2])

    return list(categories) if categories else ["unknown"]


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Получить текущего пользователя по JWT токену.
    Если токен неверный или просрочен - выбросить ошибку 401.
    """
    # user_info = get_wp_user_info(token) # При авторизации через WordPress
    user_info = get_local_user_info(token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_info


class ExternalLoginResponse(BaseModel):
    username: str
    wp_id: int
    roles: List[str]
    category: List[str]
    access_token: str
    token_type: str


@auth_router.post(
    '/authorization_wp',
    response_model=ExternalLoginResponse,
    summary="Авторизация через WordPress",
    description="Авторизует пользователя через внешний WordPress API и возвращает токен и роли."
)
async def external_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Логин пользователя через WP с помощью логина и пароля.
    Возвращает JWT токен, роли и категорию пользователя.
    """
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверные логин или пароль.')

    token = get_wp_token(username, password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректные данные для входа.')

    user_info = get_wp_user_info(token)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Не удалось получить данные пользователя.')

    roles = user_info.get("user", {}).get("roles", [])
    update_roles_in_config(db, test_wp_roles_dict)
    category = get_user_category(db, roles)

    return ExternalLoginResponse(
        username=user_info.get("name"),
        wp_id=user_info.get("id"),
        roles=roles,
        category=category,
        access_token=token,
        token_type="bearer"
    )


Conf = config.settings['authorization']
LOCAL_JWT_TOKEN = Conf["local_jwt_key"]
LOCAL_ALGORITHM = "HS256"

local_users_db = {
    "admin": {
        "name": "Администратор",
        "id": 999,
        "roles": ["administrator"],
        "category": ["administrator"]
    }
}


from pydantic import BaseModel


class SimpleLoginRequest(BaseModel):
    username: str
    password: str


from fastapi.security import OAuth2PasswordRequestForm


@auth_router.post(
    '/authorization_local',
    response_model=ExternalLoginResponse,
    summary="Локальная авторизация",
    description="Локальная авторизация для демонстрации. Логин: admin, пароль: admin"
)
async def local_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверные логин или пароль.')

    # Проверка пользователя
    if username not in local_users_db or password != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректные данные для входа.')

    # Создаем токен
    token = f"local-token-{username}-{secrets.token_hex(8)}"
    user_data = local_users_db[username]

    # Обновляем конфигурацию ролей
    update_roles_in_config(db, test_wp_roles_dict)
    category = get_user_category(db, user_data["roles"])

    return ExternalLoginResponse(
        username=user_data["name"],
        wp_id=user_data["id"],
        roles=user_data["roles"],
        category=category,
        access_token=token,
        token_type="bearer"
    )