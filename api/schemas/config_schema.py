from typing import Optional, Any
from pydantic import BaseModel, Field


class ConfigSchemaPost(BaseModel):
    name: str = Field(max_length=255)
    value: Any

    class Config:
        from_attributes = True
        extra = "forbid"


class ConfigSchemaGet(ConfigSchemaPost):
    id: int = Field(gt=0)


class ConfigSchemaUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    value: Optional[Any] = None