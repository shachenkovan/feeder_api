from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey
from database.db import Base

if TYPE_CHECKING:
    from database.models.devices_model import Devices
    from database.models.enterprises_model import Enterprises


class FilialEnterprises(Base):
    __tablename__ = 'filial_enterprises'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inn: Mapped[str] = mapped_column(String(12), ForeignKey('enterprises.inn'), nullable=False)
    adres: Mapped[str] = mapped_column(String(500), nullable=False)

    enterprises: Mapped['Enterprises'] = relationship('Enterprises', back_populates='filial_enterprise')
    device_filial: Mapped[list['Devices']] = relationship('Devices', back_populates='filial_device', cascade='delete')