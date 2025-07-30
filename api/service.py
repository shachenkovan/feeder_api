from api.routers.config_router import config_router
from api.routers.devices_router import device_router
from api.routers.enterprises_router import enterprise_router
from api.routers.filial_enterprises_router import filial_enterprise_router
from api.routers.device_models_router import device_model_router
from api.routers.regular_times_router import regular_time_router
from api.routers.task_lists_router import task_list_router
from authorization.auth import auth_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(device_model_router)
app.include_router(device_router)
app.include_router(enterprise_router)
app.include_router(filial_enterprise_router)
app.include_router(task_list_router)
app.include_router(regular_time_router)
app.include_router(config_router)
app.include_router(auth_router)