import json

from fastapi import APIRouter
from database.models import BooksInTranslation, Book, Chapter, BibleComTranslation, BibleWebsite
from database.db import Session
from sqlalchemy import and_
from services.browser import RequestBrowser

from services.downloader import BibleComDownloader as Downloader
from services.logger import logger_geneartor
from controllers.download import controller_name as download_name

logger = logger_geneartor(__name__)

controller_name = "bible"
router = APIRouter(prefix=f'/{controller_name}', tags=[f"{download_name}|{controller_name}"])

dnl = Downloader()
browser = RequestBrowser()

@router.put('/{translation_id}/books/{book_id}/chapters/{chapter_index}/html')
def download_chapter_html(translation_id: int,
                          book_id: int, 
                          chapter_index: int) -> str:
    return dnl.download_or_read_chapter(translation_id, book_id, chapter_index)

@router.put('/{translation_id}/books/{book_id}/chapters/{chapter}/txt')
def download_chapter_txt(translation_id: int, 
                         book_id: int, 
                         chapter_index: int) -> list[str]:
    if dnl.chapter_already_downloaded(translation_id, book_id, chapter_index):
        return []
    html = download_chapter_html(translation_id, book_id, chapter_index)
    parsed_verses = dnl.find_verses(html)
    with Session() as db:
        chapter = db.query(Chapter)\
            .filter(Chapter.index == chapter_index, 
                    Chapter.book_id == book_id,
                    Chapter.verses == len(parsed_verses))\
                .scalar()
    if chapter is None:
        chapter = dnl.create_chapter(chapter_index, book_id, len(parsed_verses))
    dnl.create_verses(parsed_verses, translation_id, chapter.id)
    return parsed_verses


@router.put('/{translation_id}/books/{book_id}')
def download_book(translation_id: int,
                  book_id: int) -> list[list[str]]:
    logger.info(f"Downloading book {book_id} from translation {translation_id}")
    with Session() as db:
        chapters = db.get(Book, book_id).chapters

    chapters = [download_chapter_txt(translation_id, book_id, i) for i in range(1, chapters+1)]
    return chapters

@router.put('/{translation_id}')
def download_translation(translation_id: int) -> str:
    with Session() as db:
        books_in_translation = db.query(BooksInTranslation)\
            .filter(BooksInTranslation.translation_id == translation_id)\
                .all()
    for book_in_translation in books_in_translation:
        download_book(translation_id, book_in_translation.book_id)  
    return "DONE"

@router.put('/')
def download_biblecom():
    with Session() as db:
        translations = db.query(BibleComTranslation).all()
        translations = [t for t in translations if t.id!=1] # TODO replace
        translations = [t for t in translations if t.id!=2]
    for translation in translations:
        download_translation(translation.id)
    return "DONE"



@router.put('/{translation_id}/update_book_list')
def update_books_in_translation(translation_id: int) -> list[str]:
    url = dnl.get_api_url(translation_id)
    data = json.loads(browser.get(url))
    books = data['books']
    books = [b["usfm"] for b in books]
    chapters = {book["usfm"]:[\
        len(chapters) for chapters in book["chapters"] if chapters["canonical"]\
            ] for book in data["books"]}
    with Session() as db:
        for book in books:
            book_id = db.query(Book)\
                .filter(Book.biblecom_name == book,
                        Book.chapters == len(chapters[book]))\
                    .scalar().id
            book_in_translation = db.query(BooksInTranslation)\
                .filter(BooksInTranslation.book_id==book_id,
                        BooksInTranslation.translation_id==translation_id)\
                            .all()
            if book_in_translation is None:
                db.add(BooksInTranslation(book_id=book_id, translation_id=translation_id))
        db.commit()
    return books

@router.put('/update_book_list')
def update_all_books_in_translations():
    with Session() as db:
        translations = db.query(BibleComTranslation).all()
    for translation in translations:
        update_books_in_translation(translation.id)
    return translations