import os
import re
from bs4 import BeautifulSoup
from bible_types import Verse
from download import BibleTranslation



class Cleaner:
    def __init__(self):
        pass

    def find_book(soup: BeautifulSoup) -> BeautifulSoup:
        pass

    def find_verses(soup: BeautifulSoup) -> list[Verse]:
        pass

    def clean(self, t: BibleTranslation):
        t.go_to_full_folder()
        for filename in sorted(os.listdir()):
            with open(filename, 'r') as file:
                file_data = file.read()
            book = self.find_book(file_data)
            if book is None:
                print('book_is_none', filename)
                continue
            verses = self.find_verses(book)
            t.go_to_row_folder()
            with open(filename.replace('.html', '.txt'), 'w') as file:
                for v in verses:
                    file.write(v.content + '\n')
            t.go_to_full_folder()

class BibleComCleaner(Cleaner):
    def __init__(self):
        super().__init__()

    def find_book(self, html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup.find('div', {"class": re.compile("ChapterContent_book.*")})

    def find_verses(self, soup: BeautifulSoup) -> list[Verse]:
        verses = soup.find_all('span', {"class": re.compile("ChapterContent_verse.*")})
        parsed_verses = []
        for verse in verses:
            try:
                number = verse.find('span', {"class": re.compile("ChapterContent_label.*")}).text
                content = "".join([v.text for v in verse.find_all('span', {"class": re.compile("ChapterContent_content.*")})])
                parsed_verses.append(Verse(number, content))
            except Exception:
                pass
        return parsed_verses


class BibleserverCleaner(Cleaner):
    def __init__(self):
        super().__init__()

    def find_book(self, html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup.find('article')

    def find_verses(self, soup: BeautifulSoup) -> list[Verse]:
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


if __name__ == "__main__":
    from download import list_of_bibleserver_translations
    bc = BibleserverCleaner()
    for t in list_of_bibleserver_translations:
        bc.clean(t)
    
    from download import list_of_bible_com_translations
    bc = BibleComCleaner()
    for t in list_of_bible_com_translations:
        bc.clean(t)
