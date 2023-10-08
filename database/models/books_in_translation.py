from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from database.models import Book, Translation
from database.models.base import BaseModel as Base

### Tables

class BooksInTranslation(Base):
    __tablename__ = 'books_in_translation'
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    translation_id = Column(Integer, ForeignKey(Translation.id), nullable=False)
    __table_args__ = (UniqueConstraint('book_id', 'translation_id', name='uc_book_id_translation_id'),)