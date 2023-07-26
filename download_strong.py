import os
from urllib import request
from urllib.error import HTTPError
from download import BibleComTranslation, BibleserverTranslation
from urllib.parse import quote, urlparse
from helper import headers
from bs4 import BeautifulSoup


class Verse:
    def __init__(self, book, number, chapter):
        self.book = book
        self.chapter = chapter
        self.number = number
    
    def get_bibleserver_link(self, translation: BibleserverTranslation):
        return f"https://www.bibleserver.com/{translation.name}/{self.book}{self.chapter},{self.number}"
    
    def get_biblecom_link(self, translation: BibleComTranslation):
        return f"https://www.bible.com/bible/{translation.index}/{self.book}.{self.chapter}.{self.number}"
    
    def get_biblehub_link(self):
        return f"https://biblehub.com/text/{self.book}/{self.chapter}-{self.number}.htm"
    

def get_verse_from_biblehub_link(link: str):
    parsed = urlparse(link)
    path = parsed.path
    book, chapter_verse = path.split('/')[2:4]
    chapter, verse = chapter_verse.split('-')
    verse = verse.replace('.htm', '')
    return Verse(book, chapter, verse)



class StrongWord:
    def __init__(self, original, transliteration, occurrences):
        self.original = original
        self.transliteration = transliteration
        self.occurrences = occurrences

class StrongPage:
    def __init__(self, language, number):
        self.language = language
        self.number = number
        self.url = f"https://biblehub.com/{language}/strongs_{number}.htm"

def get_strong_pages():
    hebrew_urls = [StrongPage("hebrew", i) for i in range(1, 8675)]
    greek_urls = [StrongPage("greek", i) for i in range(1, 5625)]
    return hebrew_urls + greek_urls

class StrongDownloader():
    def __init__(self):
        self.base_path = os.getcwd()
        self.folder_path = os.path.join(self.base_path, "strong")

    def go_to_folder(self):
        os.makedirs(self.folder_path, exist_ok=True)
        os.chdir(self.folder_path)

    def go_to_full_folder(self):
        path = os.path.join(self.folder_path, "full")
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def go_to_row_folder(self):
        path = os.path.join(self.folder_path, "row")
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def go_to_base_folder(self):
        os.chdir(self.base_path)

    def download(self):
        self.go_to_full_folder()
        for strong_page in get_strong_pages():
            file_name = f"{strong_page.language}_{strong_page.number}.htm"
            if os.path.exists(file_name):
                continue
            req = request.Request(quote(strong_page.url, safe=':/.'), headers=headers)
            try:
                response = request.urlopen(req)
            except HTTPError as e:
                print("could not download:", strong_page.url, e)
            data = response.read().decode()
            with open(file_name, 'w') as file:
                file.write(data)
        self.go_to_base_folder()

    def get_occurrences(self, data):
        soup = BeautifulSoup(data, "html.parser")
        return [x.text for x in soup.find_all('a', {"title": "Biblos Lexicon"})]
        

    def create_graph_data(self):
        word_nodes = []
        self.go_to_full_folder()
        for file_name in sorted(os.listdir()):
            with open(file_name, 'r') as file:
                word_id = file_name.replace(".htm", "")
                word_nodes.append(word_id)
                data = file.read()
                occ = self.get_occurrences(data)
            self.go_to_row_folder()
            with open(f"{word_id}.txt", 'w') as file:
                for o in occ:
                    file.write(o + "\n")
            self.go_to_full_folder()
        self.go_to_base_folder()

StrongDownloader().download()