from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from database.db import Base

if TYPE_CHECKING:
    from database.models.filial_enterprises_model import FilialEnterprises


class Enterprises(Base):
    __tablename__ = 'enterprises'

    inn: Mapped[str] = mapped_column(String(12), primary_key=True)
    ogrn: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    adres: Mapped[str] = mapped_column(String(500), nullable=False)

    filial_enterprise: Mapped[list['FilialEnterprises']] = relationship('FilialEnterprises', back_populates='enterprises', cascade='delete')