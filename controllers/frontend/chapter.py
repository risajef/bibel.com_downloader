import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.models import Chapter, Translation, Verse, VerseContent, Book, BooksInTranslation
from controllers.data import controller_name as data_controller_name
from database.db import Session
from services import markdown

templates = Jinja2Templates(directory="templates")

controller_name = "translation"
router = APIRouter(prefix=f'/{controller_name}', tags=[f'{data_controller_name}|{controller_name}'])

def translation_dropdown(req: Request) -> HTMLResponse:
    with Session() as db:
        translations = db.query(Translation).all()
    return templates.TemplateResponse("generic_dropdown.html", 
                                     {"request": req,
                                     "objects": translations,
                                     "dropdown_name": "translation",})

def book_dropdown(req: Request, translation_id: int) -> HTMLResponse:
    with Session() as db:
        books = db.query(BooksInTranslation).filter(BooksInTranslation.translation_id == translation_id).all()
        books = [db.get(Book, book.book_id) for book in books]

    return templates.TemplateResponse("generic_dropdown.html", 
                                     {"request": req,
                                     "objects": books,
                                     "dropdown_name": "book",})

def chapter_dropdown(req: Request, book_id: int) -> HTMLResponse:
    with Session() as db:
        chapters = db.query(Chapter).filter(Chapter.book_id == book_id).all()
        for chapter in chapters:
            chapter.name = chapter.index
            chapter.id = chapter.index
    return templates.TemplateResponse("generic_dropdown.html", 
                                     {"request": req,
                                     "objects": chapters,
                                     "dropdown_name": "chapter",})

@router.get('/{translation_id}/book/{book_id}/chapter/{chapter_index}/')
def get_chapter(chapter_index: int, translation_id: int, book_id: int, request: Request) -> HTMLResponse:
    with Session() as db:
        if not db.query(BooksInTranslation).filter(BooksInTranslation.translation_id == translation_id, BooksInTranslation.book_id == book_id).scalar():
            book_id = db.query(BooksInTranslation).filter(BooksInTranslation.translation_id == translation_id).first().book_id
            return RedirectResponse(url=f"/frontend/translation/{translation_id}/book/{book_id}/chapter/1/")
        book = db.get(Book, book_id)
        chapter = db.query(Chapter).filter(Chapter.book_id == book_id, Chapter.index == chapter_index).scalar()
        if not chapter:
            return RedirectResponse(url=f"/frontend/translation/{translation_id}/book/{book_id}/chapter/1/")
        translation = db.get(Translation, translation_id).name
        verses = db.query(Verse).filter(Verse.chapter_id == chapter.id).all()
        verses_content = db.query(VerseContent).filter(
            VerseContent.verse_id.in_([verse.id for verse in verses]),
            VerseContent.translation_id == translation_id
            ).all()
        verses_content = [vc.content for vc in verses_content]
    title = f"{translation} {book.name} {chapter.index}"

    translations_dropdown_html = translation_dropdown(req=request).body.decode('utf-8')

    book_dropdown_html = book_dropdown(translation_id=translation_id, req=request).body.decode('utf-8')

    chapter_dropdown_html = chapter_dropdown(book_id=book_id, req=request).body.decode('utf-8')
    
    print(chapter.id)
    chapter = templates.TemplateResponse("chapter.html", 
                                    {"request": request,
                                     "verses_content": verses_content, 
                                     "title": title}).body.decode('utf-8')

    return templates.TemplateResponse("main.html", 
                                      {"request": request,
                                       "content": translations_dropdown_html + book_dropdown_html + chapter_dropdown_html + chapter})
