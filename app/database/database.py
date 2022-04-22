import os
from typing import Type

from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI",
                                 SQLALCHEMY_DATABASE_URI), connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


class ModelBase:
    id = Column(Integer, primary_key=True)

    def __init__(self, *args, **kwargs):
        pass

    def save(self) -> 'Base':
        session.add(self)
        session.commit()
        return self

    @classmethod
    def get(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def list(cls):
        return session.query(cls).order_by(cls.id)

    @classmethod
    def delete(cls, id):
        return session.query(cls).filter_by(id=id).delete()


Base: Type[ModelBase] = declarative_base(cls=ModelBase)
