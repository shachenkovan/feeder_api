from datetime import time
from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# День недели: 1 (понедельник) до 7 (воскресенье)
Day = Annotated[int, Field(ge=1, le=7)]

class RegularTimesSchemaPost(BaseModel):
    """
    Pydantic-схема для создания регулярного расписания.

    Поля:
        period: Периодичность ('Еженедельно' или 'Ежедневно')
        days: Список дней недели (1 – понедельник, 7 – воскресенье).
              Для 'Ежедневно' список может быть пустым.
        timing: Время срабатывания расписания
    """
    period: Literal['Еженедельно', 'Ежедневно'] = Field(description="Периодичность ('Еженедельно' или 'Ежедневно')")
    days: Annotated[List[Day], Field(min_length=0, max_length=7)] = Field(
        description="Список дней недели (1 — понедельник, 7 — воскресенье)")
    timing: time = Field(description="Время выполнения")

    class Config:
        from_attributes = True
        extra = "forbid"


class RegularTimesSchemaGet(RegularTimesSchemaPost):
    """
    Схема для возвращаемого расписания (включает ID).
    Наследует все поля RegularTimesSchemaPost и добавляет идентификатор.
    """
    id: int = Field(gt=0, description="Уникальный идентификатор расписания в БД")


class RegularTimesSchemaUpdate(BaseModel):
    """
    Схема для частичного обновления расписания.

    Все поля являются необязательными.
    """
    period: Optional[Literal['Еженедельно', 'Ежедневно']] = Field(default=None, description="Новая периодичность")
    days: Optional[Annotated[List[Day], Field(min_length=0, max_length=7)]] = Field(
        default=None, description="Новый список дней недели")
    timing: Optional[time] = Field(default=None, description="Новое время выполнения")
