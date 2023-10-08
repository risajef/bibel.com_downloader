
import enum
from sqlalchemy import Column, String, Enum, Integer, ForeignKey, UniqueConstraint
from pydantic import BaseModel
from database.models.base import BaseModel as Base


class BibleWebsite(enum.Enum):
    bibleserver = 'bibleserver'
    biblecom = 'biblecom'
    biblehub = 'biblehub'

### Tables

class Translation(Base):
    __tablename__ = 'translations'
    name = Column(String(64), nullable=False)
    website = Column(Enum(BibleWebsite), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'website', name='uc_name_website'),)

class BibleComTranslation(Translation):
    __tablename__ = 'biblecom_translations'
    translation_id = Column(Integer, ForeignKey(Translation.id), primary_key=True, nullable=False)
    index = Column(Integer, nullable=False, unique=True)


### Pydantic Models

class PydanticTranslationGenerate(BaseModel):
    name: str
    website: BibleWebsite
    class Config:
        from_attributes = True

class PydanticTranslation(PydanticTranslationGenerate):
    id: int

class PydanticBibleComTranslation(PydanticTranslation):
    index: int