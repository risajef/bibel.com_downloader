import os
# import dictionary

stats = {}
list_of_translations = [('51','delut'),('73','hfa'),('108','ngu2011'),('158','sch51'),('877','nbh'),('65','gantp'),('58','elb71'),('57','elb'),('157','sch2000')]
list_of_translations = [('157','sch2000'),('51','delut')]

for trans in list_of_translations:

    os.chdir(trans[1] + "\\row")

    min_verse = 1000000
    min_verse_list = []
    max_verse = 0
    max_verse_list = []
    min_words = 1000000
    min_words_list = []
    max_words = 0
    max_words_list = []
    min_characters = 1000000
    min_characters_list = []
    max_characters = 0
    max_characters_list = []

    max_verse_characters = 0
    max_verse_characters_list = []
    min_verse_characters = 1000000
    min_verse_characters_list = []
    max_verse_words = 0
    max_verse_words_list = []
    min_verse_words = 1000000
    min_verse_words_list = []


    sum_chapters = 0
    sum_verse = 0
    sum_words = 0
    sum_characters = 0

    for filename in os.listdir(os.getcwd()):
        sum_chapters += 1
        file = open(filename, 'r')
        filename = filename[filename.find('_')+1:filename.find('.')]

        polished = []
        i=0
        for r in file:
            polished.append(r)
            i += 1
            number_of_words = r.count(' ')+1
            number_of_characters = r.count('')-2

            # words
            if number_of_words == min_verse_words:
                min_verse_words_list.append((filename, i))
            if number_of_words < min_verse_words:
                min_verse_words = number_of_words
                min_verse_words_list = [(filename, i)]
            if number_of_words == max_verse_words:
                max_verse_list.append((filename, i))
            if number_of_words > max_verse_words:
                max_verse_words = number_of_words
                max_verse_words_list = [(filename, i)]

            # characters
            if number_of_characters == min_verse_characters:
                min_verse_characters_list.append((filename, i))
            if number_of_characters < min_verse_characters:
                min_verse_characters = number_of_characters
                min_verse_characters_list = [(filename, i)]
            if number_of_characters == max_verse_characters:
                max_verse_characters_list.append((filename, i))
            if number_of_characters > max_verse_characters:
                max_verse_characters = number_of_characters
                max_verse_characters_list = [(filename, i)]

        number_of_verses = polished.__len__()
        number_of_words = sum([verses.count(' ') + 1 for verses in polished])
        number_of_characters = sum([verses.count('') - 2 for verses in polished])

        sum_verse += number_of_verses
        sum_words += number_of_words
        sum_characters += number_of_characters

        # verses
        if number_of_verses == min_verse:
            min_verse_list.append(filename)
        if number_of_verses < min_verse:
            min_verse = number_of_verses
            min_verse_list = [filename]
        if number_of_verses == max_verse:
            max_verse_list.append(filename)
        if number_of_verses > max_verse:
            max_verse = number_of_verses
            max_verse_list = [filename]

        # words
        if number_of_words == min_words:
            min_words_list.append(filename)
        if number_of_words < min_words:
            min_words = number_of_words
            min_words_list = [filename]
        if number_of_words == max_words:
            max_words_list.append(filename)
        if number_of_words > max_words:
            max_words = number_of_words
            max_words_list = [filename]

        # characters
        if number_of_characters == min_characters:
            min_characters_list.append(filename)
        if number_of_characters < min_characters:
            min_characters = number_of_characters
            min_characters_list = [filename]
        if number_of_characters == max_characters:
            max_characters_list.append(filename)
        if number_of_characters > max_characters:
            max_characters = number_of_characters
            max_characters_list = [filename]

    temp_stats = {'longest_chapter_(verse)': (max_verse , max_verse_list),
                  'shortest_chapter_(verse)': (min_verse , min_verse_list),
                  'longest_chapter_(words)': (max_words , max_words_list),
                  'shortest_chapter_(words)': (min_words , min_words_list),
                  'longest_chapter_(char)': (max_characters , max_characters_list),
                  'shortest_chapter_(char)': (min_characters , min_characters_list),
                  'sum_(chapters,verses,words,chars)': (sum_chapters, sum_verse, sum_words, sum_characters),
                  'longest_verse_(words)': (max_verse_words, max_verse_words_list),
                  'shortest_verse_(words)': (min_verse_words,min_verse_words_list),
                  'longest_verse_(char)': (max_verse_characters, max_verse_characters_list),
                  'shortest_verse_(char)': (min_verse_characters, min_verse_characters_list),
                  'average_verse_per_chapter': (sum_verse/float(sum_chapters)),
                  'average_words_per_chapter': (sum_words/float(sum_chapters)),
                  'average_character_per_chapter': (sum_characters/float(sum_chapters)),
                  'average_words_per_verse': (sum_words/float(sum_verse)),
                  'average_character_per_verse': (sum_characters/float(sum_verse)),
                  'average_character_per_word': (sum_characters/float(sum_words))}


    stats[trans[1]] = temp_stats


    os.chdir("..\\..\\")


True