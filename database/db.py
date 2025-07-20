from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import database


Base = declarative_base()

engine = create_engine(
    f'mysql+pymysql://{database["user"]}:{database["password"]}@{database["host"]}:{database["port"]}/{database["db"]}')
session_maker = sessionmaker(bind=engine)


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()