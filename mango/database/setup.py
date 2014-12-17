"""
Sets up the engine to connect to Danish
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE

Base = declarative_base()

engine = create_engine(
    "mysql+mysqldb://{user}:{password}@{server}/{database}?charset=utf8&use_unicode=0".format(
        user = DATABASE["user"],
        password = DATABASE["password"],
        server = DATABASE["server"],
        database = DATABASE["database"]
    )
)
Session = sessionmaker(bind=engine)

