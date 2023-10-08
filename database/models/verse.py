
from sqlalchemy import Column, Integer, ForeignKey
from .chapter import Chapter
from pydantic import BaseModel

from database.models.base import BaseModel as Base


### Tables

class Verse(Base):
    __tablename__ = 'verses'
    chapter_id = Column(Integer, ForeignKey(Chapter.id), nullable=False)
    index = Column(Integer, nullable=False)


### Pydantic models

class PydanticVerseGenerate(BaseModel):
    class Config:
        from_attributes = True
    chapter_id: int
    index: int

class PydanticVerse(PydanticVerseGenerate):
    id: int
    chapter_id: int
    index: int