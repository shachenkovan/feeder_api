from datetime import time
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Enum, JSON, Time
from typing import TYPE_CHECKING
from database.db import Base

if TYPE_CHECKING:
    from database.models.task_lists_model import TaskLists


class RegularTimes(Base):
    __tablename__ = 'regular_times'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period: Mapped[str] = mapped_column(Enum('Еженедельно', 'Ежедневно'))
    days: Mapped[dict] = mapped_column(JSON)
    timing: Mapped[time] = mapped_column(Time)

    tasks: Mapped[list['TaskLists']] = relationship('TaskLists', back_populates='reg_times', cascade='delete')