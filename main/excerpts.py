# Notes
# -----
"""
EXCERPTS:

    Holds sample English texts used for testing
    and reading.
"""

# -*- coding: utf-8 -*-

import nltk
import string
import sys

FILE_PATH = sys.path[0]


def pairTitlesTexts(titles, texts):
    """
    Initializes a dict with titles providing keys and
    texts providing values.
    ~
    Assumes titles and texts are paired and ordered.

    :return: dict, where...
        keys (str) - author and title (name) of a text
        vals (str) - text contents
    """
    books = {}
    idx = 0
    for title in titles:
        books[title] = texts[idx]
        idx += 1
    return books


def parsePlaintext(filename):
    """
    Parses plaintext file with given filename and returns a string representing
    its contents.

    :param filename: str, filename of text file
    :return: str, text file's contents
    """
    contents = []
    slash = "/" if filename[0] != "/" else ""

    with open(FILE_PATH + slash + filename, "rb") as text:
        for line in text:
            contents.append(line)

    return "".join(contents)


def parseExcerpts(filenames):
    """
        Parses plaintext files with given filenames and returns a dictionary of words
        with corresponding image file links.
        If a line in the file contains multiple words, this function splits the line
        and adds each word to the dict as separate entries linking to the same Blissymbol.
        If a word in the file has no corresponding Blissymbol, the {key,val} pair
        is not added to the output dict.

        :param filename: str, filename of text file for lexicon (each word sep. by \n)
        :return: dict, where...
            keys (str) - word in filename
            vals (str/list) - word's corresponding Blissymbol image file link(s)
        """
    books = {}

    for filename in filenames:
        title = filename[14:-4].replace("-", " ")
        books[title] = parsePlaintext(filename)

    return books


sample_texts = ["/sample texts/adams-hitchhiker's_guide.txt",
                "/sample texts/baum-wizard_of_oz.txt",
                "/sample texts/conrad-heart_of_darkness.txt",
                "/sample texts/dfw-infinite_jest.txt",
                "/sample texts/dick-electric_sheep.txt",
                "/sample texts/exupery-little_prince.txt",
                "/sample texts/exupery-petit_prince.txt",
                "/sample texts/fitzgerald-gatsby.txt",
                "/sample texts/gaiman-coraline.txt",
                "/sample texts/hesse-siddhartha.txt",
                "/sample texts/kafka-metamorphosis.txt",
                "/sample texts/machiavelli-prince.txt",
                "/sample texts/nabokov-lolita.txt",
                "/sample texts/pessoa-disquiet.txt",
                "/sample texts/pynchon-gravity's_rainbow.txt",
                "/sample texts/sagan-pale_blue_dot.txt",
                "/sample texts/salinger-catcher.txt",
                "/sample texts/vatsyayana-kama_sutra.txt"]
file_ids = [file_id for file_id in nltk.corpus.gutenberg.fileids()]
titles = [file_id[:-4].replace("-", " ") for file_id in file_ids]
texts = [" ".join(nltk.corpus.gutenberg.words(file_id)) for file_id in file_ids]
books = {}
books.update(pairTitlesTexts(titles, texts))
books.update(parseExcerpts(sample_texts))


# Fiction
alice_in_wonderland = books["carroll alice"]
moby_dick = books["melville moby_dick"]
petit_prince = books["exupery petit_prince"]
wizard_of_oz = books["baum wizard_of_oz"]
# Poetry
blake_songs = books["blake poems"]
leaves_of_grass = books["whitman leaves"]
paradise_lost = books["milton paradise"]
# Scripture
kjv = books["bible kjv"]
# Theatre
hamlet = books["shakespeare hamlet"]
julius_caesar = books["shakespeare caesar"]
macbeth = books["shakespeare macbeth"]

alice_in_wonderland_polish = 'Alicja mia\xc5\x82a ju\xc5\xbc do\xc5\x9b\xc4\x87 siedzenia na ' \
                             '\xc5\x82awce obok siostry i pr\xc3\xb3\xc5\xbcnowania. Raz czy dwa ' \
                             'razy zerkn\xc4\x99\xc5\x82a do ksi\xc4\x85\xc5\xbcki, kt\xc3\xb3r\xc4\x85 ' \
                             'czyta\xc5\x82a siostra. Niestety, w ksi\xc4\x85\xc5\xbcce nie by\xc5\x82o ' \
                             'obrazk\xc3\xb3w ani rozm\xc3\xb3w. \xe2\x80\x9eA c\xc3\xb3\xc5\xbc jest warta ' \
                             'ksi\xc4\x85\xc5\xbcka - pomy\xc5\x9bla\xc5\x82a Alicja - w kt\xc3\xb3rej nie ma ' \
                             'rozm\xc3\xb3w ani obrazk\xc3\xb3w?\xe2\x80\x9d'