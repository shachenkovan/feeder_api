from fastapi import FastAPI
from api.routers.config_router import config_router
from api.routers.devices_router import device_router
from api.routers.enterprises_router import enterprise_router
from api.routers.filial_enterprises_router import filial_enterprise_router
from api.routers.device_models_router import device_model_router
from api.routers.regular_times_router import regular_time_router
from api.routers.task_lists_router import task_list_router
from authorization.auth import auth_router

app = FastAPI(
    title="Основа API",
    description=(
        "API для управления устройствами, заданиями, расписаниями и организациями.\n\n"
        "Является основой сервиса для дистанционного кормления животных в приюте."
    )
)

# Подключение роутеров с тегами для документации
app.include_router(device_model_router, tags=["Модели устройств"])
app.include_router(device_router, tags=["Устройства"])
app.include_router(enterprise_router, tags=["Предприятия"])
app.include_router(filial_enterprise_router, tags=["Филиалы предприятий"])
app.include_router(task_list_router, tags=["Список задач"])
app.include_router(regular_time_router, tags=["Регулярные расписания"])
app.include_router(config_router, tags=["Настройки системы"])
app.include_router(auth_router, tags=["Авторизация"])
