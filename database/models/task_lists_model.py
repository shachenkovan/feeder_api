from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Enum, Boolean, DateTime, ForeignKey, CHAR
from database.db import Base

if TYPE_CHECKING:
    from database.models.devices_model import Devices
    from database.models.regular_times_model import RegularTimes


class TaskLists(Base):
    __tablename__ = 'task_lists'

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    device_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey('devices.id'), nullable=False)
    cmd: Mapped[str] = mapped_column(String(255), nullable=False)
    is_regular: Mapped[bool] = mapped_column(Boolean, default=False)
    timing: Mapped[datetime] = mapped_column(DateTime)
    regular_time_id: Mapped[int] = mapped_column(Integer, ForeignKey('regular_times.id'), nullable=True)
    status: Mapped[str] = mapped_column(Enum(
        'Ожидает',
        'Выполняется',
        'Успешно',
        'Ошибка',
        'Зарегистрировано на устройстве'), default='Ожидает')


    devices: Mapped['Devices'] = relationship('Devices', back_populates='tasks')
    reg_times: Mapped['RegularTimes'] = relationship('RegularTimes', back_populates='tasks')