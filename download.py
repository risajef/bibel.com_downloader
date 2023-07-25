import os
from urllib import request
from urllib.error import HTTPError

from bible_types import Chapter

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



class BibleTranslation:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.base_path = os.getcwd()
        self.translation_path = None
    
    def get_url(self, chapter: Chapter):
        pass

    def make_folder(self):
        os.makedirs(self.translation_path, exist_ok=True)

    def go_to_folder(self):
        path = self.translation_path
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def go_to_full_folder(self):
        path = os.path.join(self.translation_path, "full")
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def go_to_row_folder(self):
        path = os.path.join(self.translation_path, "row")
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def go_to_base_folder(self):
        os.chdir(self.base_path)

    def download(self, chapter):
        link = self.get_url(chapter)
        file_name = f"{chapter.number}_{self.name}_{chapter.name}.html"
        self.go_to_full_folder()
        if os.path.exists(file_name):
            return
        try:
            req = request.Request(link, headers=hdr)
            response = request.urlopen(req)
            data = response.read().decode()
            with open(file_name, 'w') as bible_file:
                bible_file.write(data)
        except HTTPError as e:
            print("could not download:", link, e)
        self.go_to_base_folder()

class BibleComTranslation(BibleTranslation):
    def __init__(self, index, name, description=None):
        super().__init__(name, description)
        self.index = index
        self.translation_path = os.path.join(self.base_path, "bible.com", self.name)

    def get_url(self, chapter):
        return f"https://www.bible.com/bible/{self.index}/{chapter.name}.{self.name}"
    

    
class BibleserverTranslation(BibleTranslation):
    def __init__(self, name, description=None):
        super().__init__(name, description)
        self.translation_path = os.path.join(self.base_path, "bibleserver.com", self.name)
    def get_url(self, chapter: Chapter):
        return f"https://www.bibleserver.com/{self.name}/{chapter.name}"


B = BibleComTranslation
BS = BibleserverTranslation

list_of_bible_com_translations = [
    B('51','delut',"1912"),
    B('73','hfa',),
    B('108','ngu2011'),
    B('158','sch51'),
    B('877','nbh'),
    B('65','gantp', 'Albrecht NT und Psalmen'),
    B('58','elb71', "1871"),
    B('57','elb', "unrevidiert"),
    B('157','sch2000'),
    B('877', 'BIBEL.HEUTE'),
    B('2351', 'ELBBK', 'version von bibelkommentare.de'),
    B('3100', 'LUTHEUTE'),
    B('2200', 'TKW', 'Textbibel von Kautsch und Weizsäcker'),
    ]

list_of_bibleserver_translations = [
        BS("LUT", "Luther 2017"),
        BS("DBU", "Das Buch"),
        BS("EU", "Einheitsübersetzung 2016"),
        BS("ELB", "Elberfelder Bibel"),
        BS("GNB", "Gute Nachricht Bibel 2018"),
        BS("HFA", "Hoffnung für alle"),
        BS("MENG", "Menge Bibel"),
        BS("NeÜ", "Neue evangelistische Übersetzung"),
        BS("NGÜ", "Neue Genfer Übersetzung"),
        BS("SLT", "Schlachter 2000"),
        BS("ZB", "Zürcher Bibel")
     ]

list_of_bible_translations = list_of_bible_com_translations + list_of_bibleserver_translations

if __name__ == "__main__":
    from helper import all_chapters

    for t in list_of_bible_com_translations[:2]:
        t.go_to_base_folder()
        for c in all_chapters():
            t.download(c)

    for t in list_of_bibleserver_translations[:2]:
        t.go_to_base_folder()
        for c in all_chapters():
            t.download(c)