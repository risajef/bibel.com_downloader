from urllib import request
from urllib.error import HTTPError
import os
import json
from helper import list_of_translations, save_chdir, chdir_parent

print(os.getcwd())
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}




f = open("links.txt", 'r')
i = 0

def find_all_chapters():
    chapter_list = []
    for r in f:
        if "href='" in r and "<li" in r:
            # make list of all chapters
            start = r.find("bible/546/") + 10
            end = r.find(".kjva'")
            chapter_list.append(r[start:end])
    return chapter_list


all_chapters = list(enumerate(filter(lambda x:not "intro" in x, find_all_chapters())))
for trans in list_of_translations:
    print(trans.name)
    i = 0
    save_chdir(trans.name)
    save_chdir("full")
    print(all_chapters)
    for i, chapter in all_chapters:
        link = "https://www.bible.com/bible/" + trans.index + "/" + chapter + "." + trans.name
        chapter = chapter.replace('.','')
        file_name = f"{str(i)}_{trans.name}_{chapter}.html"
        if os.path.exists(file_name):
            continue
        try:
            req = request.Request(link, headers=hdr)
            response = request.urlopen(req)
            data = response.read().decode()
            with open(file_name, 'w') as bible_file:
                bible_file.write(data)
        except HTTPError:
            print("could not download:", link)

        print(link)
    chdir_parent()
    chdir_parent()
