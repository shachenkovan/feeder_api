from datetime import time
from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated

Day = Annotated[int, Field(ge=1, le=7)]

class RegularTimesSchemaPost(BaseModel):
    period: Literal['Еженедельно', 'Ежедневно']
    days: Annotated[List[Day], Field(min_length=0, max_length=7)]
    timing: time

    class Config:
        from_attributes = True
        extra = "forbid"


class RegularTimesSchemaGet(RegularTimesSchemaPost):
    id: int = Field(gt=0)


class RegularTimesSchemaUpdate(BaseModel):
    period: Optional[Literal['Еженедельно', 'Ежедневно']] = Field(default=None)
    days: Optional[Annotated[List[Day], Field(min_length=0, max_length=7)]] = Field(default=None)
    timing: Optional[time] = Field(default=None)
