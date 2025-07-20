from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CHAR, Integer, String, ForeignKey
from database.db import Base

if TYPE_CHECKING:
    from database.models.device_models_model import DeviceModels
    from database.models.enterprises_model import FilialEnterprises
    from database.models.task_lists_model import TaskLists


class Devices(Base):
    __tablename__ = 'devices'

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('device_models.id'), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    filial_id: Mapped[int] = mapped_column(Integer, ForeignKey('filial_enterprises.id'), nullable=False)

    model: Mapped['DeviceModels'] = relationship('DeviceModels', back_populates='devices')
    filial_device: Mapped['FilialEnterprises'] = relationship('FilialEnterprises', back_populates='device_filial')
    tasks: Mapped[list['TaskLists']] = relationship('TaskLists', back_populates='devices', cascade='delete')

