from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class DeviceSchemaPost(BaseModel):
    """
    Pydantic-схема для создания устройства.

    Поля:
        model_id: ID модели устройства (целое положительное число)
        serial_number: Серийный номер устройства (макс. 50 символов)
        filial_id: ID филиала, к которому относится устройство (целое положительное число)
    """
    model_id: int = Field(gt=0, description="ID модели устройства")
    serial_number: str = Field(max_length=50, description="Серийный номер устройства")
    filial_id: int = Field(gt=0, description="ID филиала, к которому относится устройство")

    class Config:
        from_attributes = True
        extra = "forbid"


class DeviceSchemaGet(DeviceSchemaPost):
    """
    Схема для возвращаемого устройства (включает UUID).

    Наследует все поля DeviceSchemaPost и добавляет уникальный идентификатор.
    """
    id: UUID = Field(description="Уникальный идентификатор устройства (UUID)")


class DeviceSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления устройства.

    Все поля являются необязательными.
    """
    model_id: Optional[int] = Field(default=None, gt=0, description="Новый ID модели устройства")
    serial_number: Optional[str] = Field(default=None, max_length=50, description="Новый серийный номер устройства")
    filial_id: Optional[int] = Field(default=None, gt=0, description="Новый ID филиала")
