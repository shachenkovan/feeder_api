from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, conint
from typing import Literal, Optional

from sqlalchemy import Null

Day = conint(ge=1, le=7)


class TaskListsSchemaPost(BaseModel):
    device_id: UUID
    cmd: str = Field(max_length=255)
    is_regular: bool = Field(default=False)
    timing: datetime
    regular_time_id: Optional[int] = Field(default=None)
    status: Literal['Ожидает', 'Выполняется','Успешно', 'Ошибка', 'Зарегистрировано на устройстве'] = Field(default='Ожидает')


    class Config:
        from_attributes = True
        extra = "forbid"


class TaskListsSchemaGet(TaskListsSchemaPost):
    id: UUID


class TaskListsSchemaUpdate(BaseModel):
    device_id: Optional[UUID] = None
    cmd: Optional[str] = Field(default=None, max_length=255)
    is_regular: Optional[bool] = None
    timing: Optional[datetime] = None
    regular_time_id: Optional[int] = None
    status: Optional[Literal['Ожидает', 'Выполняется', 'Успешно', 'Ошибка', 'Зарегистрировано на устройстве']] = None
