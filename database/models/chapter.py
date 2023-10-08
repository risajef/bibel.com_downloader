
from sqlalchemy import Column, Integer, ForeignKey
from .book import Book

from database.models.base import BaseModel as Base


### Tables

class Chapter(Base):
    __tablename__ = 'chapters'
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    index = Column(Integer, nullable=False)
    verses = Column(Integer, nullable=False)

