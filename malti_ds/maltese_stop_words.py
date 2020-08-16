import xml.etree.ElementTree as ET
import json
import re

def convert(word):
    word = re.sub('ċ', 'c', word)
    word = re.sub('ħ', 'h', word)
    word = re.sub('ġ', 'g', word)
    word = re.sub('ż', 'ż', word)

    word = re.sub('Ċ', 'C', word)
    word = re.sub('Ħ', 'H', word)
    word = re.sub('Ġ', 'G', word)
    word = re.sub('Ż', 'Z', word)

    return word

def add_word_counts(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    for s in root.iter('s'):
        sentence = s.text.split('\n')

        for word in sentence:
    
            word = word.split('\t')[0].lower()

            word = convert(word)

            # word = re.sub('[^a-zA-Z0-9 ]', '', word) 
            regex = re.compile('[^a-zA-Z0-9 ]')
            word = regex.sub('', word) 

            if word == '':
                continue

            if word in words:
                words[word] += 1
            else:
                words[word] = 1

words = {}
add_word_counts('malti1.xml')

# Lines containing '&' were removed using regex match "^&.*"
add_word_counts('malti2.xml')

words = {k: words[k] for k in sorted(words, key=words.get, reverse=True)}
with open('maltese_word_count.json', 'w') as f:
    json.dump(words, f)