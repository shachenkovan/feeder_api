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

test_wp_roles_dict = {
    "admins": ["administrator"],
    "moders": ["editor"],
    "users": ["subscriber", "contributor", "author", "translator"]
}

def update_roles_in_config(db: Session, wp_roles: dict):
    admins_roles_in_wp = wp_roles["admins"]
    admins_roles_list = db.query(Configs).filter(Configs.name.ilike('%administrator%')).first()
    admin_roles_in_db = admins_roles_list.value
    if sorted(admin_roles_in_db) != sorted(admins_roles_in_wp):
        set_setting_value(db, 'system.roles.administrator', admins_roles_in_wp, is_force=True)

    moder_roles_in_wp = wp_roles["moders"]
    moders_roles_list = db.query(Configs).filter(Configs.name.ilike('%moderator%')).first()
    moder_roles_in_db = moders_roles_list.value
    if sorted(moder_roles_in_db) != sorted(moder_roles_in_wp):
        set_setting_value(db, 'system.roles.moderator', moder_roles_in_wp, is_force=True)

    user_roles_in_wp = wp_roles["users"]
    users_roles_list = db.query(Configs).filter(Configs.name.ilike('%user%')).first()
    user_roles_in_db = users_roles_list.value
    if sorted(user_roles_in_db) != sorted(user_roles_in_wp):
        set_setting_value(db, 'system.roles.user', user_roles_in_wp, is_force=True)




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
    update_roles_in_config(db, test_wp_roles_dict)
    category = get_user_category(db, roles)

    return {
        "username": user_info.get("name"),
        "wp_id": user_info.get("id"),
        "roles": roles,
        "category": category,
        "access_token": token,
        "token_type": "bearer"
    }

