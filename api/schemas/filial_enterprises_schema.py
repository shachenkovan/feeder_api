from typing import Optional
from pydantic import BaseModel, Field


class FilialEnterprisesSchemaPost(BaseModel):
    inn: str = Field(min_length=10, max_length=12)
    adres: str = Field(max_length=500)

    class Config:
        from_attributes = True
        extra = "forbid"


class FilialEnterprisesSchemaGet(FilialEnterprisesSchemaPost):
    id: int = Field(gt=0)


class FilialEnterprisesSchemaUpdate(BaseModel):
    inn: Optional[str] = Field(default=None, min_length=10, max_length=12)
    adres: Optional[str] = Field(default=None, max_length=500)
