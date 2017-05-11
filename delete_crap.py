import os

def ind_of_min(arr = []):
    return min([(i,e) for e,i in enumerate(arr)])[1]

def ret_index(text, str):
    i = text.find(str)
    if i == -1:
        i = 1000000000 # one billion
    return i


list_of_translations = [('51','delut'),('73','hfa'),('108','ngu2011'),('158','sch51'),('877','nbh'),('65','gantp'),('58','elb71'),('57','elb'),('157','sch2000')]
for trans in list_of_translations:
    os.chdir(trans[1])
    if not os.path.exists("row"):
        os.mkdir("row")
    os.chdir("full")




    for filename in os.listdir(os.getcwd()):
        file = open(filename, 'r')
        for row in file:
            indicator = "<div class=\"label\">"
            start = row.find(indicator)
            if start != -1:
                text = (row[start+indicator.__len__():])
                break


        chapter = int(text[:text.find("<")])

        title = "calss=\"s\">" # __len__ = 10
        remarks = "calss=\"r\">"
        verse = "calss=\"p\">"

        finished = False
        temp = ''
        polished = []
        current_verse_index = -2
        current_verse = '0\" '

        while True:
            next_verse_index = text.find("class=\"verse v")+14
            next_verse = text[next_verse_index:next_verse_index+3]
            if next_verse == current_verse:
                next_verse_index = 1000000

            start = text.find("class=\"content\">")
            if start == -1:
                break
            if next_verse_index < start and next_verse_index != 13: # new verse
                polished.append(temp)
                temp = ''
                text = text[start:]
                current_verse_index = next_verse_index
                current_verse = next_verse
            else:
                text = text[start+16:]
                end = text.find("<")
                temp = temp + text[:end]
            # print(temp)

        polished.append(temp)
        polished = polished[1:]
        for i,e in enumerate(polished):
            if e[0] == ' ':
                polished[i] = polished[i][1:]
            if e[len(e)-1] == ' ':
                polished[i] = polished[i][:len(polished[i])-1]

        for i,e in enumerate(polished):
            if polished[i] == '':
                del(polished[i])

        text = "".join(polished)

        file.close()
        os.chdir("..\\row")
        file = open('row_' + filename, 'w')
        for p in polished:
            file.write(p + '\n')
        file.close()
        os.chdir("..\\full")
        print(filename)
    os.chdir("..\\..\\")