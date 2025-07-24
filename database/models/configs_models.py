from sqlalchemy.orm import mapped_column, Mapped, declarative_base
from sqlalchemy import Integer, String, JSON

Base = declarative_base()

class Configs(Base):
    __tablename__ = 'configs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[dict] = mapped_column(JSON)
