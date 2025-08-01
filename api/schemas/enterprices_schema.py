from typing import Optional
from pydantic import BaseModel, Field


class EnterprisesSchema(BaseModel):
    """
    Pydantic-схема для создания или отображения информации о предприятии.

    Поля:
        inn: ИНН организации (от 10 до 12 символов)
        ogrn: ОГРН организации (от 13 до 15 символов)
        kpp: КПП организации (ровно 9 символов)
        name: Полное наименование предприятия (макс. 255 символов)
        adres: Юридический адрес предприятия (макс. 500 символов)
    """
    inn: str = Field(min_length=10, max_length=12, description="ИНН организации")
    ogrn: str = Field(min_length=13, max_length=15, description="ОГРН организации")
    kpp: str = Field(min_length=9, max_length=9, description="КПП организации")
    name: str = Field(max_length=255, description="Полное наименование предприятия")
    adres: str = Field(max_length=500, description="Юридический адрес предприятия")

    class Config:
        from_attributes = True
        extra = "forbid"


class EnterprisesSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления информации о предприятии.

    Все поля являются необязательными.
    """
    inn: Optional[str] = Field(default=None, min_length=10, max_length=12, description="Новый ИНН организации")
    ogrn: Optional[str] = Field(default=None, min_length=13, max_length=15, description="Новый ОГРН организации")
    kpp: Optional[str] = Field(default=None, min_length=9, max_length=9, description="Новый КПП организации")
    name: Optional[str] = Field(default=None, max_length=255, description="Новое наименование предприятия")
    adres: Optional[str] = Field(default=None, max_length=500, description="Новый юридический адрес предприятия")
