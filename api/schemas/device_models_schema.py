from pydantic import BaseModel, Field


class DeviceModelSchemaPost(BaseModel):
    """
    Pydantic-схема для создания или обновления модели устройства.

    Поля:
        name: Название модели устройства (макс. 500 символов)
    """
    name: str = Field(max_length=500, description="Название модели устройства")

    class Config:
        from_attributes = True
        extra = "forbid"


class DeviceModelSchemaGet(DeviceModelSchemaPost):
    """
    Схема для возвращаемой модели устройства (включает ID).
    Наследует все поля DeviceModelSchemaPost и добавляет идентификатор.
    """
    id: int = Field(gt=0, description="Уникальный идентификатор модели устройства в БД")
