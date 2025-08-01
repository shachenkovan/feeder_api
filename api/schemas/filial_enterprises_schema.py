from typing import Optional
from pydantic import BaseModel, Field


class FilialEnterprisesSchemaPost(BaseModel):
    """
    Pydantic-схема для создания филиала предприятия.

    Поля:
        inn: ИНН головного предприятия (от 10 до 12 символов)
        adres: Адрес филиала (макс. 500 символов)
    """
    inn: str = Field(min_length=10, max_length=12, description="ИНН головного предприятия")
    adres: str = Field(max_length=500, description="Адрес филиала")

    class Config:
        from_attributes = True
        extra = "forbid"


class FilialEnterprisesSchemaGet(FilialEnterprisesSchemaPost):
    """
    Схема для возвращаемого филиала предприятия (включает ID).
    Наследует все поля FilialEnterprisesSchemaPost и добавляет идентификатор.
    """
    id: int = Field(gt=0, description="Уникальный идентификатор филиала в БД")


class FilialEnterprisesSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления информации о филиале предприятия.

    Все поля являются необязательными.
    """
    inn: Optional[str] = Field(default=None, min_length=10, max_length=12, description="Новый ИНН головного предприятия")
    adres: Optional[str] = Field(default=None, max_length=500, description="Новый адрес филиала")
