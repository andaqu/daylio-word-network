from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from pprint import pprint
import pandas as pd
import itertools
import json
import csv
import re


def read(file):
    entries = {}
    decoded_file = file.read().decode("utf-8-sig").splitlines()
    reader = csv.DictReader(decoded_file)
    i = 0
    lines = [x for x in reader]
    for line in lines[::-1]:
        entries[i] = line
        i += 1
    return entries


def clean(entries):
    regex = re.compile("[^a-zA-Z0-9 ]")
    for key in entries:
        original_note = entries[key]["note"]
        note = original_note.lower()
        note = regex.sub("", note)
        entries[key]["note"] = note
    return entries


def add_node(nodes, e):
    if e in nodes:
        nodes[e] += 1
    else:
        nodes[e] = 1
    return nodes


def add_edge(edges, e):
    n1, n2 = e.split("_")
    same_edge = n2 + "_" + n1

    if e in edges:
        edges[e] += 1
    elif same_edge in edges:
        edges[same_edge] += 1
    else:
        edges[e] = 1
    return edges


def update_avg_mood(avg_moods, e, k):
    if e in avg_moods:
        avg_moods[e] += k
    else:
        avg_moods[e] = k
    return avg_moods


def get_maltese_stopwords(file, cutoff):
    with open("maltese\\" + file, "r") as f:
        maltese_stopwords = json.load(f)
    return [k for k in maltese_stopwords if maltese_stopwords[k] > cutoff]


def sort(dic, divide=1):
    if isinstance(divide, dict):
        return {k: dic[k] / divide[k] for k in sorted(dic, key=dic.get, reverse=True)}
    else:
        return {k: int(dic[k] / divide) for k in sorted(dic, key=dic.get, reverse=True)}


def form_network(entries):
    nodes = {}
    avg_moods = {}
    edges = {}

    new = True
    current = ""

    for key in entries:
        mood = moods[entries[key]["mood"]]
        words = entries[key]["note"].split(" ")

        for pair in itertools.product(words, words):

            if any(x in stop_words or x == "" for x in pair):
                continue

            if pair[0] != current:
                current = pair[0]
                nodes = add_node(nodes, current)
                avg_moods = update_avg_mood(avg_moods, current, mood)
                new = True

            if pair[0] == pair[1] and new:
                new = False
                continue

            edges = add_edge(edges, pair[0] + "_" + pair[1])

    return sort(nodes), sort(edges, divide=2), sort(avg_moods, divide=nodes)


def init_stopwords(lang):
    # obtained from: https://gist.github.com/sebleier/554280
    global stop_words
    if "English" in lang:
        stop_words.extend(
            [
                "i",
                "me",
                "my",
                "myself",
                "we",
                "our",
                "ours",
                "ourselves",
                "you",
                "your",
                "yours",
                "yourself",
                "yourselves",
                "he",
                "him",
                "his",
                "himself",
                "she",
                "her",
                "hers",
                "herself",
                "it",
                "its",
                "itself",
                "they",
                "them",
                "their",
                "theirs",
                "themselves",
                "what",
                "which",
                "who",
                "whom",
                "this",
                "that",
                "these",
                "those",
                "am",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "being",
                "have",
                "has",
                "had",
                "having",
                "do",
                "does",
                "did",
                "doing",
                "a",
                "an",
                "the",
                "and",
                "but",
                "if",
                "or",
                "because",
                "as",
                "until",
                "while",
                "of",
                "at",
                "by",
                "for",
                "with",
                "about",
                "against",
                "between",
                "into",
                "through",
                "during",
                "before",
                "after",
                "above",
                "below",
                "to",
                "from",
                "up",
                "down",
                "in",
                "out",
                "on",
                "off",
                "over",
                "under",
                "again",
                "further",
                "then",
                "once",
                "here",
                "there",
                "when",
                "where",
                "why",
                "how",
                "all",
                "any",
                "both",
                "each",
                "few",
                "more",
                "most",
                "other",
                "some",
                "such",
                "no",
                "nor",
                "not",
                "only",
                "own",
                "same",
                "so",
                "than",
                "too",
                "very",
                "s",
                "t",
                "can",
                "will",
                "just",
                "don",
                "should",
                "now",
            ]
        )
    if "Maltese" in lang:
        stop_words.extend(get_maltese_stopwords("maltese_word_count.json", 1000))


def init_moods():
    global moods
    moods = {"rad": 5, "great": 4, "good": 3, "okay": 2, "sad": 1}


stop_words = []
moods = {}

