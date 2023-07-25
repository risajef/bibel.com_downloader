import os
import re
from bs4 import BeautifulSoup

class Chapter:
    def __init__(self, number, name):
        self.number = number
        self.name = name

def chdir_parent():
    os.chdir(os.path.dirname(os.getcwd()))

def save_chdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

def find_book(text: str) -> BeautifulSoup:
    soup = BeautifulSoup(text, "html.parser")
    return soup.find('div', {"class": re.compile("ChapterContent_book.*")})


def find_all_chapters():
    chapter_list = []
    with open("links.txt", 'r') as f:
        for r in f:
            if "href='" in r and "<li" in r:
                # make list of all chapters
                start = r.find("bible/546/") + 10
                end = r.find(".kjva'")
                chapter_list.append(r[start:end])
    return chapter_list

def all_chapters():
    if os.path.exists("all_chapters.txt"):
        with open("all_chapters.txt", 'r') as f:
            data = f.readlines()
            data = [d[:-1] for d in data]
        data = [row.split(",") for row in data]
        chapters = [Chapter(int(row[0]), row[1]) for row in data]
        return chapters
    
    chapters = list(enumerate(filter(lambda x:not "intro" in x, find_all_chapters())))
    with open("all_chapters.txt", 'w') as f:
        for c in chapters:
            f.write(f"{c[0]},{c[1]}\n")
    return all_chapters()