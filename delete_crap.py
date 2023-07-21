import os
import re
from bs4 import BeautifulSoup
from helper import chdir_parent, find_book

class Translation:
    def __init__(self, index, name):
        self.index = index
        self.name = name

T = Translation
list_of_translations = [
    T('51','delut'),
    T('73','hfa'),
    T('108','ngu2011'),
    T('158','sch51'),
    T('877','nbh'),
    T('65','gantp'),
    T('58','elb71'),
    T('57','elb'),
    T('157','sch2000')]

def make_folders_in_translation(translation: str):
    os.chdir(translation)
    if not os.path.exists("row"):
        os.mkdir("row")

class Verse:
    def __init__(self, number, content):
        self.number = number
        self.content = content


def find_verses(soup: BeautifulSoup) -> list[Verse]:
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

def remove_empty_files():

    for trans in list_of_translations:
        print(trans.name)
        make_folders_in_translation(trans.name)
        
        for filename in sorted(os.listdir("full")):
            os.chdir("full")
            with open(filename, 'r') as file:
                file_data = file.read()
            book = find_book(file_data)
            
            if book is None:
                os.remove(filename)
            chdir_parent()
        chdir_parent()


def do():
    for trans in list_of_translations:
        make_folders_in_translation(trans.name)
        for filename in sorted(os.listdir("full")):
            os.chdir("full")
            with open(filename, 'r') as file:
                file_data = file.read()
            book = find_book(file_data)
            if book is None:
                chdir_parent()
                print(filename)
                continue
            verses = find_verses(book)

            chdir_parent()
            os.chdir("row")
            with open(f"row_{filename}", 'w') as file:
                for v in verses:
                    file.write(v.content + '\n')
            chdir_parent()
        chdir_parent()

remove_empty_files()
do()