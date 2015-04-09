# -*- coding: utf-8 -*-

word_mapping = {}

def load_traditional_to_simplified(dict_filename):
    dict_file = open(dict_filename)
    for line in dict_file:
        columns = line.strip().decode('utf-8').split('\t')
        if len(columns) != 2:
            continue
        word_mapping[columns[0]] = columns[1]
    dict_file.close()

def get_simplified_word(word):
    if word not in word_mapping:
        return word
    return word_mapping[word]

def get_simplified_words(words):
    vec = []
    for word in words:
        vec.append(get_simplified_word(word))
    return ''.join(vec)

load_traditional_to_simplified("../data/traditional_to_simplified.txt")

if __name__ == "__main__":
    print get_simplified_words(u"美圖秀秀")
    print 'done...'
