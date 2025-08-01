from typing import Optional, Any
from pydantic import BaseModel, Field


class ConfigSchemaPost(BaseModel):
    """
    Pydantic схема для создания или обновления настройки.

    Поля:
        name: Уникальное имя настройки (макс. 255 символов)
        value: Значение настройки (любой допустимый тип)
    """
    name: str = Field(max_length=255, description="Уникальное имя настройки")
    value: Any = Field(description="Значение настройки")

    class Config:
        from_attributes=True
        extra="forbid"


class ConfigSchemaGet(ConfigSchemaPost):
    """
    Схема для возвращаемой настройки (включает ID).
    Наследует все поля ConfigSchemaPost и добавляет идентификатор.
    """
    id: int = Field(gt=0, description="Уникальный идентификатор настройки в БД")


class ConfigSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления настройки.
    Все поля опциональны.
    """
    name: Optional[str] = Field(max_length=255, description="Новое имя настройки")
    value: Optional[Any] = Field(description="Новое значение")