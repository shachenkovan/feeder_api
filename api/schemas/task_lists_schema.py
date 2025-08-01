from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, conint
from typing import Literal, Optional


class TaskListsSchemaPost(BaseModel):
    """
    Pydantic-схема для создания задания в списке задач.

    Поля:
        device_id: Идентификатор устройства (UUID)
        cmd: Команда, отправляемая на устройство (макс. 255 символов)
        is_regular: Признак регулярного задания (по умолчанию False)
        timing: Время выполнения задания
        regular_time_id: ID записи в таблице регулярных расписаний (если применимо)
        status: Текущий статус задания
                Возможные значения: 'Ожидает', 'Выполняется', 'Успешно', 'Ошибка',
                'Зарегистрировано на устройстве'
    """
    device_id: UUID = Field(description="UUID устройства, на которое отправляется задание")
    cmd: str = Field(max_length=255, description="Команда, отправляемая на устройство")
    is_regular: bool = Field(default=False, description="Является ли задание регулярным")
    timing: datetime = Field(description="Время выполнения задания")
    regular_time_id: Optional[int] = Field(default=None, description="ID регулярного расписания (если задано)")
    status: Literal[
        'Ожидает', 'Выполняется', 'Успешно', 'Ошибка', 'Зарегистрировано на устройстве'
    ] = Field(default='Ожидает', description="Статус выполнения задания")

    class Config:
        from_attributes = True
        extra = "forbid"


class TaskListsSchemaGet(TaskListsSchemaPost):
    """
    Схема для возвращаемого задания из списка задач (включает ID).
    Наследует все поля TaskListsSchemaPost и добавляет уникальный идентификатор.
    """
    id: UUID = Field(description="Уникальный идентификатор задания (UUID)")


class TaskListsSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления задания.

    Все поля являются необязательными.
    """
    device_id: Optional[UUID] = Field(default=None, description="Новый UUID устройства")
    cmd: Optional[str] = Field(default=None, max_length=255, description="Новая команда")
    is_regular: Optional[bool] = Field(default=None, description="Обновлённый признак регулярности")
    timing: Optional[datetime] = Field(default=None, description="Новое время выполнения")
    regular_time_id: Optional[int] = Field(default=None, description="Новый ID регулярного расписания")
    status: Optional[Literal[
        'Ожидает', 'Выполняется', 'Успешно', 'Ошибка', 'Зарегистрировано на устройстве'
    ]] = Field(default=None, description="Новый статус задания")
