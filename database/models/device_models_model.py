from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String
from database.db import Base

if TYPE_CHECKING:
    from database.models.devices_model import Devices

class DeviceModels(Base):
    __tablename__ = 'device_models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)

    devices: Mapped[list['Devices']] = relationship('Devices', back_populates='model', cascade='delete')
