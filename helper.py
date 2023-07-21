import os
import re
from bs4 import BeautifulSoup

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

def chdir_parent():
    os.chdir(os.path.dirname(os.getcwd()))

def save_chdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

def find_book(text: str) -> BeautifulSoup:
    soup = BeautifulSoup(text, "html.parser")
    return soup.find('div', {"class": re.compile("ChapterContent_book.*")})