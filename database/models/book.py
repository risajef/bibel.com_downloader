
from sqlalchemy import Column, String, Integer
from pydantic import BaseModel
from database.models import BaseModel as Base

### Tables

class Book(Base):
    __tablename__ = 'books'
    name = Column(String(64), nullable=False)
    bibleserver_name = Column(String(64), nullable=True)
    biblecom_name = Column(String(64), nullable=True)
    biblehub_name = Column(String(64), nullable=True)
    chapters = Column(Integer, nullable=False, default=0)


### Pydantic Models

class PydanticBookGenerate(BaseModel):
    name: str
    bibleserver_name: str | None
    biblecom_name: str | None
    biblehub_name: str | None
    class Config:
        from_attributes = True

class PydanticBook(PydanticBookGenerate):
    id: int
