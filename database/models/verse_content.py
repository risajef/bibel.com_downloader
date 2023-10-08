
from sqlalchemy import Column, Integer, ForeignKey, String
from .verse import Verse
from .translation import Translation

from database.models.base import BaseModel as Base


### Tables

class VerseContent(Base):
    __tablename__ = 'verses_content'
    verse_id = Column(Integer, ForeignKey(Verse.id), nullable=False)
    translation_id = Column(Integer, ForeignKey(Translation.id), nullable=False)
    content = Column(String, nullable=False)

