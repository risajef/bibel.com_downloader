import json
from dataclasses import dataclass
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.models.translation import BibleWebsite
from services.browser import RequestBrowser, SeleniumBrowser
from database.models import Book, BibleComTranslation, Translation, BooksInTranslation
from database.db import Session

router = APIRouter(prefix='/setup', tags=['setup'])

@dataclass
class BookNames():
    name: str
    bibleserver: str = None
    biblehub: str = None
    biblecom: str = None

book_names: list[BookNames] = [
    BookNames(name="Genesis", biblehub="genesis", biblecom="GEN", bibleserver="Genesis"),
    BookNames(name="Exodus", biblehub="exodus", biblecom="EXO", bibleserver="Exodus"),
    BookNames(name="Leviticus", biblehub="leviticus", biblecom="LEV", bibleserver="Leviticus"),
    BookNames(name="Numbers", biblehub="numbers", biblecom="NUM", bibleserver="Numbers"),
    BookNames(name="Deuteronomy", biblehub="deuteronomy", biblecom="DEU", bibleserver="Deuteronomy"),
    BookNames(name="Joshua", biblehub="joshua", biblecom="JOS", bibleserver="Joshua"),
    BookNames(name="Judges", biblehub="judges", biblecom="JDG", bibleserver="Judges"),
    BookNames(name="Ruth", biblehub="ruth", biblecom="RUT", bibleserver="Ruth"),
    BookNames(name="1 Samuel", biblehub="1_samuel", biblecom="1SA", bibleserver="1 Samuel"),
    BookNames(name="2 Samuel", biblehub="2_samuel", biblecom="2SA", bibleserver="2 Samuel"),
    BookNames(name="1 Kings", biblehub="1_kings", biblecom="1KI", bibleserver="1 Kings"),
    BookNames(name="2 Kings", biblehub="2_kings", biblecom="2KI", bibleserver="2 Kings"),
    BookNames(name="1 Chronicles", biblehub="1_chronicles", biblecom="1CH", bibleserver="1 Chronicles"),
    BookNames(name="2 Chronicles", biblehub="2_chronicles", biblecom="2CH", bibleserver="2 Chronicles"),
    BookNames(name="Ezra", biblehub="ezra", biblecom="EZR", bibleserver="Ezra"),
    BookNames(name="Nehemiah", biblehub="nehemiah", biblecom="NEH", bibleserver="Nehemiah"),
    BookNames(name="Esther", biblehub="esther", biblecom="EST", bibleserver="Esther"),
    BookNames(name="Job", biblehub="job", biblecom="JOB", bibleserver="Job"),
    BookNames(name="Psalms", biblehub="psalms", biblecom="PSA", bibleserver="Psalms"),
    BookNames(name="Proverbs", biblehub="proverbs", biblecom="PRO", bibleserver="Proverbs"),
    BookNames(name="Ecclesiastes", biblehub="ecclesiastes", biblecom="ECC", bibleserver="Ecclesiastes"),
    BookNames(name="Song of Solomon", biblehub="songs", biblecom="SNG", bibleserver="Song of Solomon"),
    BookNames(name="Isaiah", biblehub="isaiah", biblecom="ISA", bibleserver="Isaiah"),
    BookNames(name="Jeremiah", biblehub="jeremiah", biblecom="JER", bibleserver="Jeremiah"),
    BookNames(name="Lamentations", biblehub="lamentations", biblecom="LAM", bibleserver="Lamentations"),
    BookNames(name="Ezekiel", biblehub="ezekiel", biblecom="EZK", bibleserver="Ezekiel"),
    BookNames(name="Daniel", biblehub="daniel", biblecom="DAN", bibleserver="Daniel"),
    BookNames(name="Hosea", biblehub="hosea", biblecom="HOS", bibleserver="Hosea"),
    BookNames(name="Joel", biblehub="joel", biblecom="JOL", bibleserver="Joel"),
    BookNames(name="Amos", biblehub="amos", biblecom="AMO", bibleserver="Amos"),
    BookNames(name="Obadiah", biblehub="obadiah", biblecom="OBA", bibleserver="Obadiah"),
    BookNames(name="Jonah", biblehub="jonah", biblecom="JON", bibleserver="Jonah"),
    BookNames(name="Micah", biblehub="micah", biblecom="MIC", bibleserver="Micah"),
    BookNames(name="Nahum", biblehub="nahum", biblecom="NAM", bibleserver="Nahum"),
    BookNames(name="Habakkuk", biblehub="habakkuk", biblecom="HAB", bibleserver="Habakkuk"),
    BookNames(name="Zephaniah", biblehub="zephaniah", biblecom="ZEP", bibleserver="Zephaniah"),
    BookNames(name="Haggai", biblehub="haggai", biblecom="HAG", bibleserver="Haggai"),
    BookNames(name="Zechariah", biblehub="zechariah", biblecom="ZEC", bibleserver="Zechariah"),
    BookNames(name="Malachi", biblehub="malachi", biblecom="MAL", bibleserver="Malachi"),
    BookNames(name="Matthew", biblehub="matthew", biblecom="MAT", bibleserver="Matthew"),
    BookNames(name="Mark", biblehub="mark", biblecom="MRK", bibleserver="Mark"),
    BookNames(name="Luke", biblehub="luke", biblecom="LUK", bibleserver="Luke"),
    BookNames(name="John", biblehub="john", biblecom="JHN", bibleserver="John"),
    BookNames(name="Acts", biblehub="acts", biblecom="ACT", bibleserver="Acts"),
    BookNames(name="Romans", biblehub="romans", biblecom="ROM", bibleserver="Romans"),
    BookNames(name="1 Corinthians", biblehub="1_corinthians", biblecom="1CO", bibleserver="1 Corinthians"),
    BookNames(name="2 Corinthians", biblehub="2_corinthians", biblecom="2CO", bibleserver="2 Corinthians"),
    BookNames(name="Galatians", biblehub="galatians", biblecom="GAL", bibleserver="Galatians"),
    BookNames(name="Ephesians", biblehub="ephesians", biblecom="EPH", bibleserver="Ephesians"),
    BookNames(name="Philippians", biblehub="philippians", biblecom="PHP", bibleserver="Philippians"),
    BookNames(name="Colossians", biblehub="colossians", biblecom="COL", bibleserver="Colossians"),
    BookNames(name="1 Thessalonians", biblehub="1_thessalonians", biblecom="1TH", bibleserver="1 Thessalonians"),
    BookNames(name="2 Thessalonians", biblehub="2_thessalonians", biblecom="2TH", bibleserver="2 Thessalonians"),
    BookNames(name="1 Timothy", biblehub="1_timothy", biblecom="1TI", bibleserver="1 Timothy"),
    BookNames(name="2 Timothy", biblehub="2_timothy", biblecom="2TI", bibleserver="2 Timothy"),
    BookNames(name="Titus", biblehub="titus", biblecom="TIT", bibleserver="Titus"),
    BookNames(name="Philemon", biblehub="philemon", biblecom="PHM", bibleserver="Philemon"),
    BookNames(name="Hebrews", biblehub="hebrews", biblecom="HEB", bibleserver="Hebrews"),
    BookNames(name="James", biblehub="james", biblecom="JAS", bibleserver="James"),
    BookNames(name="1 Peter", biblehub="1_peter", biblecom="1PE", bibleserver="1 Peter"),
    BookNames(name="2 Peter", biblehub="2_peter", biblecom="2PE", bibleserver="2 Peter"),
    BookNames(name="1 John", biblehub="1_john", biblecom="1JN", bibleserver="1 John"),
    BookNames(name="2 John", biblehub="2_john", biblecom="2JN", bibleserver="2 John"),
    BookNames(name="3 John", biblehub="3_john", biblecom="3JN", bibleserver="3 John"),
    BookNames(name="Jude", biblehub="jude", biblecom="JUD", bibleserver="Jude"),
    BookNames(name="Revelation", biblehub="revelation", biblecom="REV", bibleserver="Revelation"),
    BookNames(name="Tobit", biblecom="TOB"),
    BookNames(name="Judith", biblecom="JDT"),
    BookNames(name="Esther (Additions)", biblecom="ESG"),
    BookNames(name="Wisdom of Solomon", biblecom="WIS"),
    BookNames(name="Ecclesiasticus", biblecom="SIR"),
    BookNames(name="Baruch", biblecom="BAR"),
    BookNames(name="The Three Holy Children", biblecom="S3Y"),
    BookNames(name="Susanna", biblecom="SUS"),
    BookNames(name="Bel and the Dragon", biblecom="BEL"),
    BookNames(name="1 Maccabees", biblecom="1MA"),
    BookNames(name="2 Maccabees", biblecom="2MA"),
]

@dataclass
class TranslationHelper:
    name: str
    description: str | None = None

@dataclass
class BibleComTranslationHelper:
    index: str
    name: str
    description: str | None = None

T = TranslationHelper
BT = BibleComTranslationHelper

list_of_bible_com_translations = [
    BT('546', 'KJVAAE', 'King James Version with Apocrypha, American Edition'),
    BT('51','delut', "Lutherbibel 1912"),
    BT('57','elb', "unrevidiert"),
    BT('58','elb71', "Elberfelder Bibel 1871"),
    BT('65','gantp', 'Albrecht NT und Psalmen'),
    BT('73','hfa', 'Hoffnung für alle'),
    BT('108','ngu2011', 'Neue Genfer Übersetzung'),
    BT('157','sch2000', 'Schlachter 2000'),
    BT('158','sch51', 'Schlachter 1951'),
    BT('877', 'BIBEL.HEUTE', 'Bibel Heute'),
    BT('2200', 'TKW', 'Textbibel von Kautsch und Weizsäcker'),
    BT('2351', 'ELBBK', 'version von bibelkommentare.de'),
    BT('3100', 'LUTHEUTE', 'Lutherbibel 2017'),
    ]

list_of_bibleserver_translations = [
        T("DBU", "Das Buch"),
        T("EU", "Einheitsübersetzung 2016"),
        T("ELB", "Elberfelder Bibel"),
        T("GNB", "Gute Nachricht Bibel 2018"),
        T("HFA", "Hoffnung für alle"),
        T("LUT", "Luther 2017"),
        T("MENG", "Menge Bibel"),
        T("NeÜ", "Neue evangelistische Übersetzung"),
        T("NGÜ", "Neue Genfer Übersetzung"),
        T("SLT", "Schlachter 2000"),
        T("ZB", "Zürcher Bibel")
     ]

list_of_biblehub_translations = [
    T("interlinear"),
]

@router.put('/put_translations')
def put_translations():
    try:
        with Session() as db:
            for translation in list_of_bible_com_translations:
                db.add(BibleComTranslation(
                    index=translation.index, 
                    name=translation.name, 
                    website=BibleWebsite.biblecom))
            for translation in list_of_bibleserver_translations:
                db.add(Translation(
                    name=translation.name,
                    website=BibleWebsite.bibleserver))
            for translation in list_of_biblehub_translations:
                db.add(Translation(
                    name=translation.name, 
                    website=BibleWebsite.biblehub))
            db.commit()
        return "success"
    except IntegrityError as e:
        return f"You probably already added this translations. {e}"

@router.put('/put_books_and_book_in_biblehub_translation')
def put_books_and_book_in_biblehub_translation():
    book_name_map = {b.biblehub:b.name for b in book_names}
    with Session() as db:
        translations = db.query(Translation)\
            .filter(Translation.website == BibleWebsite.biblehub)\
                .all()
    for translation in translations:
        url = f"https://biblehub.com/{translation.name}/cmenus/genesis/1.htm"
        browser = RequestBrowser()
        data = browser.get(url)
        soup = BeautifulSoup(data, 'html.parser')
        soup = soup.find('select', {'name': 'select1'})
        options = soup.find_all('option')
        books = [option["value"] for option in options]
        books = [book.replace("../../", "").replace("/1.htm", "") for book in books]

        for book in books:
            url = f"https://biblehub.com/{translation.name}/cmenus/{book}/1.htm"
            data = browser.get(url)
            soup = BeautifulSoup(data, 'html.parser')
            soup = soup.find('select', {'name': 'select2'})
            options = soup.find_all('option')
            chapter_names = [option["value"] for option in options]
            chapter_names = [option.replace(f"../../{book}/", "").replace(".htm", "") for option in chapter_names]
            db_book = db.query(Book).filter(Book.name==book_name_map[book], Book.chapters==len(chapter_names)).first()
            if db_book is None:
                db_book = Book(name=book, biblehub_name=book, chapters=len(chapter_names))
                db.add(db_book)
            else:
                db_book.biblehub_name = book
            db.commit()


@router.put('/put_books_and_book_in_biblecom_translation')
def put_books_and_book_in_biblecom_translation():
    book_name_map = {b.biblecom:b.name for b in book_names}
    with Session() as db:
        translations = db.query(BibleComTranslation).all()
    assert all([t.website == BibleWebsite.biblecom for t in translations])
    for translation in translations:
        url = f"https://www.bible.com/api/bible/version/{translation.index}"
        browser = RequestBrowser()
        data = json.loads(browser.get(url))
        books = data['books']
        for book in books:
            if book["usfm"] == "S3Y" and translation.index == "546":
                continue # This is because bible com says it has this book but it doesn't
            book_usfm = book["usfm"]
            chapters = book["chapters"]
            chapters = [c for c in chapters if c["canonical"] is True]
            db_book = db.query(Book).filter(
                Book.name == book_name_map[book_usfm],
                Book.chapters == len(chapters)).first()
            # Add book
            if db_book is None:
                db_book = Book(name=book_name_map[book_usfm], biblecom_name=book_usfm, chapters=len(chapters))
                db.add(db_book)
            else:
                db_book.biblecom_name = book_usfm
            db.commit()
            books_in_translation = db.query(BooksInTranslation).filter(
                BooksInTranslation.book_id == db_book.id,
                BooksInTranslation.translation_id == translation.id).first()
            if books_in_translation is None:
                db.add(BooksInTranslation(book_id=db_book.id, translation_id=translation.id))
            db.commit()
        db.commit()
    return "success"


@router.put('/put_books_and_book_in_bibleserver_translation')
def put_books_and_book_in_bibleserver_translation():
    with Session() as db:
        translations = db.query(Translation)\
            .filter(Translation.website == BibleWebsite.bibleserver)\
                .all()
    browser = SeleniumBrowser()
    for translation in translations:
        url = f"https://www.bibleserver.com/{translation.name}/Matth%C3%A4us1"
        data = browser.get(url)
        print(data)
        break
    return "SUCCESS"
    #     books = data['books']
    #     for book in books:
    #         book_usfm = book["usfm"]
    #         book_name = book["human"]
    #         chapters = book["chapters"]
    #         chapters = [c for c in chapters if c["canonical"] is True]
    #         db_book = db.query(Book).filter(
    #             Book.biblecom_name == book_usfm,
    #             Book.chapters == len(chapters)).first()
    #         if db_book is None:
    #             # Add book
    #             db_book = Book(name=book_name, biblecom_name=book_usfm, chapters=len(chapters))
    #             db.add(db_book)
    #             db.commit()
    #         books_in_translation = db.query(BooksInTranslation).filter(
    #             BooksInTranslation.book_id == db_book.id,
    #             BooksInTranslation.translation_id == translation.id).first()
    #         if books_in_translation is None:
    #             db.add(BooksInTranslation(book_id=db_book.id, translation_id=translation.id))
    #         db.commit()
    #     db.commit()
    # return "success"


@router.put('/cold_start')
def cold_start():
    put_translations()
    # put_books_and_book_in_biblehub_translation()
    put_books_and_book_in_biblecom_translation()
    # put_books_and_book_in_bibleserver_translation()