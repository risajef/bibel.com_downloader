import datetime
from sqlalchemy import Column, DateTime, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def update(self, updated_object):
        for key, value in updated_object.dict().items():
            setattr(self, key, value)
        return self