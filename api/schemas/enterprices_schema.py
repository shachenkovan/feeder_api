from typing import Optional

from pydantic import BaseModel, Field


class EnterprisesSchema(BaseModel):
    inn: str = Field(min_length=10, max_length=12)
    ogrn: str = Field(min_length=13, max_length=15)
    kpp: str = Field(min_length=9, max_length=9)
    name: str = Field(max_length=255)
    adres: str = Field(max_length=500)


    class Config:
        from_attributes = True
        extra = "forbid"


class EnterprisesSchemaUpdate(BaseModel):
    inn: Optional[str] = Field(default=None, min_length=10, max_length=12)
    ogrn: Optional[str] = Field(default=None, min_length=13, max_length=15)
    kpp: Optional[str] = Field(default=None, min_length=9, max_length=9)
    name: Optional[str] = Field(default=None, max_length=255)
    adres: Optional[str] = Field(default=None, max_length=500)
