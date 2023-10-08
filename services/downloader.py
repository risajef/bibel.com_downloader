from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod
from fastapi import HTTPException
from sqlalchemy import and_

from database.db import Session
from database.models import Book, Chapter, Verse, Translation, BibleComTranslation, VerseContent, BibleWebsite
from services.browser import RequestBrowser
from services.fileManager import FileManager
from services.logger import logger_geneartor

logger = logger_geneartor(__name__)


class AbstractDownloader(ABC):
    @abstractmethod
    def get_url(self, translation: Translation, book: Book, chapter_index: int):
        """
        Returns the url of the chapter in a book for a translation in the database.
        """

    @abstractmethod
    def download_or_read_chapter(self, translation_id: int, book_id: int, chapter_index: int) -> str:
        """
        Downloads the chapter if not already downloaded
        """

    @abstractmethod
    def find_verses(self, html: str) -> list[str]:
        """
        Given the html of a chapter return a list of strings. Where each string is a verse.
        """

    @abstractmethod
    def create_chapter(self, index: int, book_id: int, verses: int) -> Chapter:
        """
        Creates the required chapter in the database
        """

    @abstractmethod
    def create_verse(self, index: int, chapter_id: int):
        """
        Create the required verse in the database
        """

    @abstractmethod
    def create_verse_content(self, verse_id: int, translation_id: int, content: str):
        """
        Add the content of the verse to the database.
        """

    @abstractmethod
    def create_verses(self, verses: list[str], translation_id: int, chapter_id: int):
        """
        Creates all verses given where the index in the verses list is interpreted as the verse number.
        """

    @abstractmethod
    def chapter_already_downloaded(self, translation_id: int, book_id: int, chapter: int) -> bool:
        """
        Returns if a given chapter is already downloaded. Where the chapter is given as an index and not an id.
        """
    

class BaseDownloader:
    def create_chapter(self, index: int, book_id: int, verses: int) -> Chapter:
        with Session() as db:
            chapter = db.query(Chapter)\
                .filter(Chapter.index == index,
                        Chapter.book_id == book_id,
                        Chapter.verses == verses).scalar()
            if chapter is None:
                chapter = Chapter(index=index, book_id=book_id, verses=verses)
                db.add(chapter)
            db.commit()
            db.refresh(chapter)
        return chapter

    def create_verse(self, index: int, chapter_id: int):
        with Session() as db:
            verse = db.query(Verse)\
                .filter(Verse.index == index, 
                        Verse.chapter_id == chapter_id)\
                            .scalar()
            if verse is None:
                verse = Verse(index=index, chapter_id=chapter_id)
                db.add(verse)
            db.commit()
            db.refresh(verse)
        return verse

    def create_verse_content(self, verse_id: int, translation_id: int, content: str):
        with Session() as db:
            verse_content = db.query(VerseContent)\
                .filter(VerseContent.verse_id == verse_id,
                        VerseContent.translation_id == translation_id)\
                            .scalar()
            if verse_content is None:
                verse_content = VerseContent(verse_id=verse_id, 
                                             translation_id=translation_id, 
                                             content=content)
                db.add(verse_content)
            db.commit()
            db.refresh(verse_content)
        return verse_content

    def create_verses(self, verses: list[str], translation_id: int, chapter_id: int):
        with Session() as db:
            translation = db.query(BibleComTranslation)\
                .filter(BibleComTranslation.id == translation_id)\
                    .scalar()
        if translation is None:
            raise HTTPException(status_code=404, detail="Translation not found")
        for index, content in enumerate(verses):
            verse = self.create_verse(index, chapter_id)
            self.create_verse_content(verse.id, translation_id, content)

    def chapter_already_downloaded(self, translation_id: int, book_id: int, chapter: int) -> bool:
        with Session() as db:
            chapters = db.query(Chapter)\
                .filter(Chapter.index == chapter, 
                        Chapter.book_id == book_id)\
                            .all()
            if len(chapters) == 0:
                return False
            chapter_ids = [chapter.id for chapter in chapters]
            verses = db.query(Verse).filter(Verse.chapter_id.in_(chapter_ids)).all()
            if len(verses) == 0:
                return False
            verse_ids = set([verse.id for verse in verses])
            verse_content = db.query(VerseContent)\
                .filter(VerseContent.verse_id.in_(verse_ids), 
                        VerseContent.translation_id == translation_id).first()
            if verse_content is None:
                fm = FileManager()
                translation = db.get(Translation, translation_id)
                book = db.get(Book, book_id)
                fm.file_exists(translation, book, chapter)
                return False
        return True
    
    def download_if_necessary(self, translation_id: int, book_id: int, chapter_index: int):
        fm = FileManager()
        with Session() as db:
            translation = db.get(Translation, translation_id)
            if translation.website == BibleWebsite.biblecom:
                translation = db.get(BibleComTranslation, translation_id)
            book = db.get(Book, book_id)
        if fm.file_exists(translation, book, chapter_index):
            return
        url = self.get_url(translation, book, chapter_index)
        browser = RequestBrowser()
        data = browser.get(url)
        fm.write_data_to_file(data, translation, book, chapter_index)
        logger.info("Downloaded from website")
        return
    
    def download_or_read_chapter(self, translation_id: int, book_id: int, chapter_index: int) -> str:
        fm = FileManager()
        with Session() as db:
            translation = db.get(Translation, translation_id)
            if translation.website == BibleWebsite.biblecom:
                translation = db.get(BibleComTranslation, translation_id)
            book = db.get(Book, book_id)
        if not fm.file_exists(translation, book, chapter_index):
            self.download_if_necessary(translation_id, book_id, chapter_index)

        data = fm.read_file(translation, book, chapter_index)
        logger.info(f"Read from file: translation_id: {translation_id}, book_id: {book_id}, chapter_index: {chapter_index}")
        return data
    
    def get_url(self, translation: Translation, book: Book, chapter_index: int):
        raise NotImplementedError("get_url not implemented")

class BibleComDownloader(BaseDownloader, AbstractDownloader):
    def get_url(self, translation: BibleComTranslation, book: Book, chapter_index: int):
        if book.biblecom_name == "ESG":
            chapter_index = f"{chapter_index}_1"
        if book.biblecom_name == "SIR":
            if chapter_index == 1:
                chapter_index = "1_1"
            elif chapter_index == 2:
                chapter_index = "1_2"
            else:
                chapter_index -= 1
        if book.biblecom_name == "SUS":
            chapter_index = f"{chapter_index}_1"
        return f"https://www.bible.com/bible/{translation.index}/{book.biblecom_name}.{chapter_index}.{translation.name}"

    def find_verses(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.find('div', {"class": re.compile("ChapterContent_book.*")})
        verses = soup.find_all('span', {"class": re.compile("ChapterContent_verse.*")})
        parsed_verses = []
        for verse in verses:
            try:
                verse.find('span', {"class": re.compile("ChapterContent_label.*")}).text
                content = "".join([v.text for v in verse.find_all('span', {"class": re.compile("ChapterContent_content.*")})])
                parsed_verses.append(content)
            except Exception as e:
                logger.debug(e)
        return parsed_verses

    def get_api_url(self, translation_id):
        with Session() as db:
            translation = db.get(BibleComTranslation, translation_id)
        return f"https://www.bible.com/api/bible/version/{translation.index}"
    

class BibleserverDownloader(BaseDownloader, AbstractDownloader):
    def get_url(self, translation: Translation, book: Book, chapter_index: int):
        return f"https://www.bibleserver.com/{translation.name}/{book.bibleserver_name}/{chapter_index}"

    def find_verses(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        soup =  soup.find('article')
        verses = soup.find_all('span', {"class": "verse"})
        parsed_verses = []
        for v in verses:
            try:
                number = v.find('span', {"class": "verse-number"}).text
                content = v.find('span', {"class": "verse-content"}).text
                parsed_verses.append(Verse(number, content))
            except Exception:
                pass
        return parsed_verses

    def get_api_url(self, translation_id):
        with Session() as db:
            translation = db.get(BibleComTranslation, translation_id)
        return f"https://www.bible.com/api/bible/version/{translation.index}"
    
class BibleHubStrongDownloader(BaseDownloader, AbstractDownloader):
    def get_url(self, translation: Translation, book: Book, chapter_index: int):
        assert translation.website == BibleWebsite.biblehub
        assert translation.name == "interlinear"
        return f"https://biblehub.com/{translation.name}/{book.biblehub_name}/{chapter_index}.htm"

class GenericDownloader(BaseDownloader, AbstractDownloader):
    def __init__(self, website: BibleWebsite):
        match website:
            case BibleWebsite.biblecom:
                self._downloader = BibleComDownloader()
            case BibleWebsite.bibleserver:
                raise NotImplementedError("Bibleserver is not implemented for now.")

    def get_api_url(self, *args, **kwargs):
        return self._downloader.get_api_url(*args, **kwargs)

    def get_url(self, *args, **kwargs):
        return self._downloader.get_url(*args, **kwargs)

    def download_or_read_chapter(self, *args, **kwargs) -> str:
        return self._downloader.download_or_read_chapter(*args, **kwargs)

    def find_verses(self, *args, **kwargs) -> list[str]:
        return self._downloader.find_verses(*args, **kwargs)
