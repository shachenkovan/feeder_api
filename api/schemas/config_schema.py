from typing import Optional
from pydantic import BaseModel, Field


class ConfigSchemaPost(BaseModel):
    name: str = Field(max_length=255)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True
        extra = "forbid"


class ConfigSchemaGet(ConfigSchemaPost):
    id: int = Field(gt=0)

