import urllib2 as url
import os

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

list_of_translations = [('51','delut'),('73','hfa'),('108','ngu2011'),('158','sch51'),('877','nbh'),('65','gantp'),('58','elb71'),('57','elb'),('157','sch2000')]


f = open("links.txt", 'r')
i = 0
chapter_list = []
for r in f:
    if "href='" in r and "<li" in r:
        # make list of all chapters
        start = r.find("bible/546/") + 6
        end = r.find(".kjva'")
        chapter_list.append(r[start:end])
for trans in list_of_translations:
    i = 0
    if not os.path.exists(trans[1]):
        os.makedirs(trans[1])
    os.chdir(trans[1])
    if not os.path.exists("full"):
        os.makedirs("full")
    os.chdir("full")
    for c in chapter_list:
        link = "https://www.bible.com/de/bible/" + trans[0] + "/" + c + "." + trans[1]
        c = c.replace('.','')
        file_name = str(i) + "_" + trans[1] + "_" + c + '.html'
        try:
            req = url.Request(link, headers=hdr)
            response = url.urlopen(req)
            data = response.read()
            bible_file = open(file_name, 'w')
            bible_file.write(data)
            bible_file.close()
        except url.HTTPError:
            print("could not download:", link)

        print(link)
        i+=1
    os.chdir('..\\..\\')
