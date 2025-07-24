from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


Base = declarative_base()

engine = create_engine(
    f'mysql+pymysql://{settings["database"]["user"]}:{settings["database"]["password"]}@{settings["database"]["host"]}:{settings["database"]["port"]}/{settings["database"]["db"]}')
session_maker = sessionmaker(bind=engine)


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()