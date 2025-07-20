from pydantic import BaseModel, Field


class DeviceModelSchemaPost(BaseModel):
    name: str = Field(max_length=500)

    class Config:
        from_attributes = True
        extra = "forbid"


class DeviceModelSchemaGet(DeviceModelSchemaPost):
    id: int = Field(gt=0)

