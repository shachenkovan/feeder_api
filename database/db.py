from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


Base = declarative_base()

DBConf = settings['database']
engine = create_engine(
    f'mysql+pymysql://{DBConf["user"]}:{DBConf["password"]}@{DBConf["host"]}:{DBConf["port"]}/{DBConf["db"]}')
session_maker = sessionmaker(bind=engine)


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()