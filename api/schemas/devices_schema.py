from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class DeviceSchemaPost(BaseModel):
    model_id: int = Field(gt=0)
    serial_number: str = Field(max_length=50)
    filial_id: int = Field(gt=0)

    class Config:
        from_attributes = True
        extra = "forbid"


class DeviceSchemaGet(DeviceSchemaPost):
    id: UUID


class DeviceSchemaUpdate(BaseModel):
    model_id: Optional[int] = Field(default=None, gt=0)
    serial_number: Optional[str] = Field(default=None, max_length=50)
    filial_id: Optional[int] = Field(default=None, gt=0)
