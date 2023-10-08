import os
from bible_types import Chapter

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def find_all_chapters():
    chapter_list = []
    print(os.getcwd())
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