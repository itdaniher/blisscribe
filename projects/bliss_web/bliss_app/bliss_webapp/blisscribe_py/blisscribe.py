# -*- coding: utf-8 -*-
"""
BLISSCRIBE:

    A Python module for translating text to Blissymbols.

    All relevant parts-of-speech tags (used throughout) and
    their meanings are enumerated here:
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
import collections
import os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from pattern import text
from pattern.text import en, es, fr, de, it, nl, tag
from PIL import Image, ImageDraw, ImageFont, ImageChops
from fpdf import FPDF

try:
    from parse_lexica import LexiconParser
except ImportError:
    print("Parse_lexica module could not be imported.\n\
    Please find the local module parse_lexica.py \n\
    and relocate it to the same directory as blisscribe.py.")
else:
    from parse_lexica import LexiconParser


class BlissTranslator:
    """
    A class for translating text in select languages to Blissymbols.
    ~
    Currently supported languages:
        - English (default)
        - Spanish
        - German
        - French
        - Italian
        - Dutch
        - Polish
    ~
    Begin by initializing a BlissTranslator with a supported language.
    Pass a string in your chosen language to translate() for an output
    PDF of the given text with Blissymbols.
    ~
    Use chooseTranslatables() to set whether to translate nouns,
    verbs, adjectives, and/or other parts of speech.
    ~
    By default, a BlissTranslator will translate all parts of
    speech in CHOSEN_POS, i.e., nouns, verbs, and adjectives.
    To translate all other parts of speech, set self.other to True.
    ~
    Contains methods for:
        1) selecting which parts of speech to translate
           --> chooseTranslatables()
           --> chooseNouns()
           --> chooseVerbs()
           --> chooseAdjs()
           --> chooseOtherPOS()
        2) selecting whether to translate text to Blissymbols
           immediately or gradually
           --> setFastTranslate()
        3) selecting font & font size for output PDF translations
           --> setFont()
        4) selecting whether to subtitle all Blissymbols or only
           new Blissymbols
           --> setSubAll()
    """
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    # Fonts
    ROMAN_FONT = "/Library/Fonts/Times New Roman.ttf"
    SANS_FONT = "/Library/Fonts/Arial.ttf"
    HIP_FONT = "/Library/Fonts/Helvetica.dfont"
    BLISS_FONT = "/Users/courtney/Library/Fonts/Blissymbolics.ttf"
    FONT_FAMS = {"Times New Roman": ROMAN_FONT,
                 "Arial": SANS_FONT,
                 "Helvetica": HIP_FONT,
                 "Blissymbols": BLISS_FONT}
    DEFAULT_FONT_SIZE = 30
    # Images
    IMG_PATH = FILE_PATH + "/symbols/png/full/"
    IMAGES_SAVED = 0
    # Language
    STARTING_PUNCT = set(["(", '"', "-",
                          "\xe2\x80\x9c", "\xe2\x80\x98", "\xe2\x80\x9e"])  # spaces BEFORE
    ENDING_PUNCT = set([".", ",", ";", ":", "?", "!", ")", '"', "-",
                        "\xe2\x80\x9d", "\xe2\x80\x99", u"\u201d"])  # spaces AFTER
    PUNCTUATION = STARTING_PUNCT.union(ENDING_PUNCT)
    PUNCTUATION.add("'")
    WHITESPACE = set(["\n", '', ' '])
    PARTS_OF_SPEECH = set(["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS",
                           "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$",
                           "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG",
                           "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"])
    POS_KEY = {"CC": "Coordinating conjunction",
               "CD": "Cardinal number",
               "DT": "Determiner",
               "EX": "Existential there",
               "FW": "Foreign word",
               "IN": "Preposition or subordinating conjunction",
               "JJ": "Adjective",
               "JJR": "Adjective, comparative",
               "JJS": "Adjective, superlative",
               "LS": "List item marker",
               "MD": "Modal",
               "NN": "Noun, singular or mass",
               "NNS": "Noun, plural",
               "NNP": "Proper noun, singular",
               "NNPS": "Proper noun, plural",
               "PDT": "Predeterminer",
               "POS": "Possessive ending",
               "PRP": "Personal pronoun",
               "PRP$": "Possessive pronoun",
               "RB": "Adverb",
               "RBR": "Adverb, comparative",
               "RBS": "Adverb, superlative",
               "RP": "Particle",
               "SYM": "Symbol",
               "TO": "to",
               "UH": "Interjection",
               "VB": "Verb, base form",
               "VBD": "Verb, past tense",
               "VBG": "Verb, gerund or present participle",
               "VBN": "Verb, past participle",
               "VBP": "Verb, non-3rd person singular present",
               "VBZ": "Verb, 3rd person singular present",
               "WDT": "Wh-determiner",
               "WP": "Wh-pronoun",
               "WP$": "Possessive wh-pronoun",
               "WRB": "Wh-adverb"}
    DEFAULT_POS = set(["NN", "NNS", "VB", "VBD", "VBG", "VBN", "JJ", "JJR", "JJS"])
    CHOSEN_POS = DEFAULT_POS
    LANG_CODES = {"Arabic": "arb",
                  "Bulgarian": 'bul',
                  "Catalan": 'cat',
                  "Danish": 'dan',
                  'German': 'deu',
                  "Greek": 'ell',
                  "English": 'eng',
                  "Basque": 'eus',
                  "Persian": 'fas',
                  "Finnish": 'fin',
                  "French": 'fra',
                  "Galician": 'glg',
                  "Hebrew": 'heb',
                  "Croatian": 'hrv',
                  "Indonesian": 'ind',
                  "Italian": 'ita',
                  "Japanese": 'jpn',
                  "Norwegian Nyorsk": 'nno',
                  "Norwegian Bokmal": 'nob',
                  "Polish": 'pol',
                  "Portuguese": 'por',
                  "Chinese": "qcn",
                  "Slovenian": 'slv',
                  "Spanish": 'spa',
                  "Swedish": 'swe',
                  "Thai": 'tha',
                  "Malay": 'zsm'}
    WORDNET_LANGS = set(LANG_CODES.keys())
    DEFAULT_LANG = "English"
    LEX_PARSER = LexiconParser()
    SUPPORTED_LANGS = WORDNET_LANGS.intersection(LEX_PARSER.LANGUAGES)
    PATTERN_LANGS = text.LANGUAGES

    def __init__(self, language="English", font_path=SANS_FONT, font_size=DEFAULT_FONT_SIZE):
        # Fonts
        self.font_size = font_size
        self.font_path = font_path
        self.font = ImageFont
        self.setFont(self.font_path, self.font_size)
        # Images
        self.image_heights = self.font_size*3
        self.pages = []
        self.sub_all = False
        self.page_nums = True
        # Language
        self.bliss_dict = dict
        self.polish_lexicon = dict
        self.language = str
        self.lang_code = str
        self.setLanguage(language)
        self.fast_translate = False
        self.words_seen = dict
        self.words_changed = dict
        self.initSeenChanged()
        self.defns_chosen = {}  # holds user choices for correct word definitions
        # --> parts of speech
        self.nouns = True
        self.verbs = True
        self.adjs = True
        self.other = False

    # GETTERS/SETTERS
    # ===============
    def getFont(self, font_path, font_size):
        """
        Returns an ImageFont with given font_path and font_size.
        ~
        If font_path is invalid, returns an ImageFont using this
        BlissTranslator's ROMAN_FONT and font_size.

        :param font_path: str, path to font file
        :param font_size: int, desired font size
        :return: ImageFont, font with given path and font size
        """
        try:
            ImageFont.truetype(font_path, font_size)
        except IOError:
            self.font_path = self.ROMAN_FONT
            return ImageFont.truetype(self.ROMAN_FONT, font_size)
        else:
            return ImageFont.truetype(font_path, font_size)

    def setFont(self, font_path, font_size):
        """
        Sets this BlissTranslator's default font to an ImageFont
        with given font_path and font_size.
        ~
        If font_path is invalid, uses BlissTranslator's ROMAN_FONT.

        :param font_path: str, path to font file
        :param font_size: int, desired font size
        :return: None
        """
        self.font = self.getFont(font_path, font_size)

    def setLanguage(self, language):
        """
        Sets this BlissTranslator's native language
        to the input language.
        ~
        If given language is invalid, do not change this
        BlissTranslator's default language.

        :param language: str, language to set to default
        :return: None
        """
        try:
            self.LEX_PARSER.getDefns(self.LEX_PARSER.LEX_PATH, language)
        except KeyError or IOError:
            self.language = "English"
        else:
            self.language = language
        finally:
            self.lang_code = self.LANG_CODES[self.language]
            if self.lang_code not in wordnet.langs():
                self.getMultiLingualLemmas()
            self.setBlissDict()

    def getMultiLingualLemmas(self):
        """
        Assumes this BlissTranslator's language isn't part of
        default WordNet, and tries to load a custom tab file
        in the given language to WordNet instead.
        ~
        If no such file can be loaded, raises an Exception.
        ~
        Used to add non-default OMWs to WordNet.

        :return: None
        """
        assert self.lang_code not in wordnet.langs()

        tab_file = self.LEX_PARSER.getTabFile(self.lang_code)

        if tab_file is not None:
            wordnet.custom_lemmas(tab_file, self.lang_code)
        else:
            raise Exception("Blisscribe doesn't support this language yet... oops!")

    def initBlissDict(self):
        """
        Returns a Bliss dictionary in this BlissTranslator's
        set language.

        :return: dict, where...
            keys (str) - words in desired language
            vals (str) - corresponding Blissymbol image filenames
        """
        return self.LEX_PARSER.getDefnImgDict(self.LEX_PARSER.LEX_PATH, self.language)

    def setBlissDict(self):
        """
        Initializes this BlissTranslator's bliss_dict in
        its native language.

        :return: None
        """
        self.bliss_dict = self.initBlissDict()

        if self.language == "Polish":
            self.polish_lexicon = self.LEX_PARSER.parseLexicon("/resources/lexica/polish.txt")

    def initSeenChanged(self):
        """
        Initializes this BlissTranslator's words_seen
        as a default dict.

        :return: None
        """
        self.words_seen = collections.defaultdict(bool)
        self.words_changed = collections.defaultdict(bool)

    def setSubAll(self, sub_all):
        """
        Sets self.sub_all equal to input sub_all value.
        ~
        Setting sub_all to True will produce subtitles under
        all words translated to Blissymbols.
        Setting sub_all to False will produce subtitles only
        under new words translated to Blissymbols.
        ~
        Sets subtitle settings for this BlissTranslator's
        translate() method.

        :param sub_all: bool, whether to subtitle all words
        :return: None
        """
        self.sub_all = sub_all

    def setPageNums(self, page_nums):
        """
        Sets self.page_nums to page_nums.
        ~
        Setting page_nums to True will cause this
        BlissTranslator to enumerate the bottom of each
        PDF page from translate().
        Setting page_nums to False will result in no page
        numbers.

        :param page_nums: bool, whether to enumerate
            translated PDF pages
        :return: None
        """
        self.page_nums = page_nums

    def setFastTranslate(self, fast_translate):
        """
        Set's self.fast_translate to fast_translate.
        ~
        Setting fast_translate to True will cause this
        BlissTranslator to translate the first instances of
        every word.
        Setting fast_translate to False will cause it to
        only translate a word after having seen it once.
        ~
        Sets translation speed for this BlissTranslator's
        translate() method.

        :param fast_translate: bool, whether to translate
            words to Blissymbols immediately
        :return: None
        """
        self.fast_translate = fast_translate

    def setTranslatables(self):
        """
        Resets CHOSEN_POS according to this BlissTranslator's translatables
        (i.e., nouns, verbs, adjs, and other).

        :return: None
        """
        if self.other:
            # adds all non-default parts of speech
            self.CHOSEN_POS = self.PARTS_OF_SPEECH
        else:
            self.CHOSEN_POS = set()
            if self.nouns:
                self.CHOSEN_POS.add("NN")
                self.CHOSEN_POS.add("NNS")
            if self.verbs:
                self.CHOSEN_POS.add("VB")
                self.CHOSEN_POS.add("VBD")
                self.CHOSEN_POS.add("VBG")
                self.CHOSEN_POS.add("VBN")
            if self.adjs:
                self.CHOSEN_POS.add("JJ")
                self.CHOSEN_POS.add("JJR")
                self.CHOSEN_POS.add("JJS")

    def chooseNouns(self, nouns):
        """
        Allows user to set whether to translate nouns.

        :param nouns: bool, True to translate nouns
        :return: None
        """
        self.nouns = nouns
        self.setTranslatables()

    def chooseVerbs(self, verbs):
        """
        Allows user to set whether to translate verbs.

        :param verbs: bool, True to translate verbs
        :return: None
        """
        self.verbs = verbs
        self.setTranslatables()

    def chooseAdjs(self, adjs):
        """
        Allows user to set whether to translate adjectives.

        :param adjs: bool, True to translate adjectives
        :return: None
        """
        self.adjs = adjs
        self.setTranslatables()

    def chooseOtherPOS(self, other):
        """
        Allows user to set whether to translate all other
        parts of speech.

        :param other: bool, True to translate other parts of speech
        :return: None
        """
        self.other = other
        self.setTranslatables()

    def chooseTranslatables(self, nouns, verbs, adjs, other):
        """
        Allows user to set whether to translate nouns, verbs,
        adjectives, and/or all other parts of speech.
        ~
        Changes this BlissTranslator's variables with the same names.

        :param nouns: bool, True to translate nouns
        :param verbs: bool, True to translate verbs
        :param adjs: bool, True to translate adjectives
        :param other: bool, True to translate all other parts of speech
        :return: None
        """
        self.chooseNouns(nouns)
        self.chooseVerbs(verbs)
        self.chooseAdjs(adjs)
        self.chooseOtherPOS(other)
        self.setTranslatables()

    def isSeen(self, word):
        """
        Returns True if the given word is part of the
        words_seen dict.

        :param word: str, word to check if in words_seen
        :return: bool, whether given word is in words_seen
        """
        return self.words_seen[word]

    def addSeen(self, word):
        """
        Adds word to words_seen dict.

        :param word: str, word to add to words_seen
        :return: None
        """
        self.words_seen[word] = True

    def isChanged(self, word):
        """
        Returns True if the given word is part of the
        words_changed dict.

        :param word: str, word to check if in words_changed
        :return: bool, whether given word is in words_changed
        """
        return self.words_changed[word]

    def addChanged(self, word):
        """
        Adds word to words_changed dict.

        :param word: str, word to add to words_changed
        :return: None
         """
        self.words_changed[word] = True

    # IMAGES
    # ======
    def getWordWidth(self, word):
        """
        Returns the width of the given string or Image in pixels.

        :param word: str or Image
        :return: int, word width in pixels
        """
        if word == "\n":
            return 0
        elif type(word) == str:
            return self.trimHorizontal(self.getWordImg(word, self.font_size)).size[0]
        else:
            try:
                return word.size[0]
            except AttributeError:
                return self.font_size

    def makeBlankImg(self, x, y):
        """
        Returns a blank (white) image of dimensions x and y.

        :param x: int, x-dimension of image
        :param y: int, y-dimension of image
        :return: Image, blank image
        """
        return Image.new("RGBA", (x, y), (255, 255, 255, 255))

    def getWordImg(self, word, font_size=DEFAULT_FONT_SIZE):
        """
        Draws and returns an Image of given word in given font_size.

        :param word: str, word to render to Image
        :param font_size: int, desired font size for string
        :return: Image, image of input str
        """
        img = self.makeBlankImg(len(word) * font_size,
                                self.image_heights)
        if word == "\n":
            return img
        else:
            word = self.unicodize(word)
            sketch = ImageDraw.Draw(img)
            sketch.text((0, font_size),
                        word,
                        font=ImageFont.truetype(font=self.font_path, size=font_size),
                        fill="black")
            return self.trimHorizontal(img)

    def getBlissImg(self, word, max_width, max_height, choosing=False):
        """
        Draws and returns a thumbnail Image of the given word's
        Blissymbol, with width not exceeding max_width.
        ~
        If a word has multiple meanings, then return the Blissymbol
        corresponding to the first meaning listed in bliss_dict.

        :param word: str, word to render to Image
        :param max_width: int, maximum width of Image (in pixels)
        :param max_height: int, maximum height of Image (in pixels)
        :param choosing: bool, whether user can choose definitions for
            ambiguous words
        :return: Image, image of input str's Blissymbol
        """
        trim = False

        if word == "indicator (plural)":
            trim = True
            img_fname = "indicator_(plural).png"
        else:
            try:
                self.bliss_dict[word]
            except KeyError:
                if self.isTranslatable(word):
                    lexeme = self.getLexeme(word)
                elif self.isSynonymTranslatable(word):
                    lexeme = self.translateUntranslatable(word)
                else:
                    return self.makeBlankImg(1,1)
            else:
                lexeme = word
            img_fname = self.bliss_dict[lexeme]

            if type(img_fname) == list:
                if choosing:
                    choice = self.chooseDefn(lexeme)
                else:
                    choice = 0
                img_fname = img_fname[choice]

        bliss_word = Image.open(str(self.IMG_PATH + img_fname))
        img = bliss_word

        #if trim:
        #    img = self.trim(img)
        #else:
        img = img.crop(box=(0, 190, img.width, img.height-90))
        img.thumbnail((max_width, max_height))
        return img

    def getSubbedBlissImg(self, word, max_width, max_height, subs=True):
        """
        Returns the given word as a Blissymbol with subtitles
        in this BlissTranslator's chosen language.
        ~
        If subs is set to False, output Image has no subtitles, but
        still offsets as if there were.

        :param word: str, word to translate & subtitle
        :param max_width: int, max width of output image
        :param max_height: int, max height of output image
        :param subs: bool, whether to subtitle output image
        :return: Image, subtitled Blissymbol image
        """
        bg = self.makeBlankImg(max_width, max_height)
        bliss_word = self.getBlissImg(word, max_width, int(max_height/2))
        start_x = max_width / 2
        start_y = self.font_size * 2
        space = self.getMinSpace()
        sub_size = self.getSubtitleSize()

        # bliss_word = self.trimHorizontal(bliss_word)
        text_word = self.getWordImg(word.upper(), font_size=sub_size)
        word = self.unicodize(word)
        text_word = self.trim(text_word)

        text_width = text_word.size[0]
        bliss_width = bliss_word.size[0]
        bliss_height = bliss_word.size[1]

        start_bliss_word_x = start_x - (bliss_width / 2)
        start_bliss_word_y = start_y - space - bliss_height  # above origin pt
        start_text_word_x = start_x - (text_width / 2)
        start_text_word_y = start_y + space  # below origin pt

        bg.paste(bliss_word, (start_bliss_word_x, start_bliss_word_y))

        if subs:
            sketch = ImageDraw.Draw(bg)
            sketch.text((start_text_word_x, start_text_word_y),
                        word.upper(),
                        font=ImageFont.truetype(font=self.font_path, size=sub_size),
                        fill="black")

        return self.trimHorizontal(bg)

    def getPluralImg(self, img):
        """
        Returns the given Blissymbol image with the plural
        Blissymbol at the end.

        :param img: Image, Blissymbol image to pluralize
        :return: Image, input image pluralized
        """
        # plural = self.getBlissImg("indicator (plural)", img.size[0], img.size[1]/2)
        plural = self.getSubbedBlissImg("indicator (plural)", img.size[0], img.size[1], subs=False)
        bg = self.makeBlankImg(img.size[0] + plural.size[0], self.image_heights)
        bg.paste(img, (0, 0))
        bg.paste(plural, (bg.size[0] - plural.size[0], 0))
        return bg

    def trim(self, img):
        """
        Trims the input image's whitespace.

        :param img: Image, image to be trimmed
        :return: Image, trimmed image

        Taken from http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil/29192070.
        """
        bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()

        if bbox:
            return img.crop(bbox)
        else:
            return img

    def trimHorizontal(self, img):
        """
        Trims the input image's whitespace only
        in the x-dimension.

        :param img: Image, image to be trimmed
        :return: Image, trimmed image

        Adapted from http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil/29192070.
        """
        bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        bbox = (bbox[0], 0, bbox[2], img.height)

        if bbox:
            return img.crop(bbox)
        else:
            return img

    def trimHorizontalStd(self, img, std):
        """
        Trims input image's whitespace in x-dimension
        and crops image in y-dimension to fit std,
        then returns the result.

        :param img: Image, image to be trimmed
        :return: Image, trimmed image

        Adapted from http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil/29192070.
        """
        bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        bbox = (bbox[0], 0, bbox[2], min(std, img.height))

        if bbox:
            return img.crop(bbox)
        else:
            return img

    def incLine(self, line_no, inc=DEFAULT_FONT_SIZE * 3):
        """
        Returns current line_no multiplied by inc to get the
        y-coordinate for this line in pixels.

        :param line_no: int, the current line number
        :param inc: int, factor to multiply line_no by
        :return: int, y-coordinate for this line (in px)
        """
        return line_no * inc

    def getSubtitleSize(self):
        """
        Returns a font size suitable as a subtitle for this
        BlissTranslator's default font_size.

        :return: int, subtitle font size
        """
        return self.font_size - int(self.font_size / 2)

    def getSpaceSize(self):
        """
        Returns an appropriate space size relative to this
        BT's font_size in pixels.

        :return: int, space size (in pixels)
        """
        return int(self.font_size / 1.5)

    def getMinSpace(self):
        """
        Returns the minimum spacing between characters
        in pixels.

        Useful for standardizing punctuation spacing.

        :return: int, minimum space size (in pixels)
        """
        return 2

    def drawAlphabet(self, words, columns=10):
        """
        Returns alphabet-style definition image containing each word in words,
        with word definition on bottom and corresponding Blissymbol on top.
        ~
        If a word in words has no corresponding Blissymbol, this method does
        not draw it.

        :param words: str, words (separated by spaces) to render
        :param columns: int, maximum number of columns
        :return: Image, drawn alphabet of given words
        """
        # TODO: standardize image sizes in BlissTranslator to simplify rendering
        # TODO: refactor translate() & drawAlphabet() for less repetition
        words_list = words.split(" ")

        glyph_bg_wh = self.image_heights
        start_x = glyph_bg_wh / 2
        start_y = self.font_size * 2
        space = self.getMinSpace()

        bliss_alphabet = []

        for word in words_list:
            bg = self.makeBlankImg(glyph_bg_wh, glyph_bg_wh)

            if self.canBeTranslated(word):
                try:
                    self.bliss_dict[word]
                except KeyError:
                    if self.isTranslatable(word):
                        lexeme = self.getLexeme(word)
                    else:
                        lexeme = self.translateUntranslatable(word)
                    bliss_word = self.getBlissImg(lexeme, glyph_bg_wh, glyph_bg_wh / 2)
                else:
                    bliss_word = self.getBlissImg(word, glyph_bg_wh, glyph_bg_wh / 2)

                # bliss_word = self.trim(bliss_word)
                text_word = self.getWordImg(word.upper(), font_size=self.getSubtitleSize())
                text_word = self.trimHorizontal(text_word)

                text_width = text_word.width
                bliss_width = bliss_word.width
                bliss_height = bliss_word.height

                start_bliss_word_x = start_x - (bliss_width / 2)
                start_bliss_word_y = start_y - space - bliss_height  # above origin pt
                start_text_word_x = start_x - (text_width / 2)
                start_text_word_y = start_y + space  # below origin pt

                bg.paste(text_word, (start_text_word_x, start_text_word_y))
                bg.paste(bliss_word, (start_bliss_word_x, start_bliss_word_y))

            bliss_alphabet.append(bg)

        alphabet_bg_width = glyph_bg_wh * min(len(bliss_alphabet), columns)
        alphabet_bg_height = glyph_bg_wh * (len(bliss_alphabet) / columns + 1)
        alphabet_bg = self.makeBlankImg(alphabet_bg_width, alphabet_bg_height)
        indent = 0
        line_height = 0

        for defn in bliss_alphabet:
            if (indent + glyph_bg_wh) > alphabet_bg_width:
                indent = 0
                line_height += 1

            if (line_height * glyph_bg_wh) > alphabet_bg_height:
                alphabet_bg.show()
                alphabet_bg = self.makeBlankImg(alphabet_bg_width, alphabet_bg_height)

            alphabet_bg.paste(defn, (indent, self.incLine(line_height, glyph_bg_wh)))
            indent += glyph_bg_wh

        try:
            self.trimHorizontal(alphabet_bg)
        except TypeError:
            return alphabet_bg
        else:
            if len(bliss_alphabet) > columns:
                return self.trimHorizontal(alphabet_bg)
            else:
                return self.trimHorizontalStd(alphabet_bg, self.image_heights)

    def displayImages(self, pages):
        """
        Displays each image in pages.

        :param pages: List[Image], images to display
        :return: None
        """
        for page in pages:
            page.show()

    def saveImages(self, pages):
        """
        Saves each image in pages as a .png file.
        ~
        Names each image beginning at this BlissTranslator's
        IMAGES_SAVED variable and incrementing by 1.
        ~
        After loop terminates, sets IMAGES_SAVED to the
        final accumulated value.
        ~
        Returns a list of the image filenames created.

        :param pages: List[Image], images to save to file
        :return: None
        """
        filenames = []
        start = self.IMAGES_SAVED

        for page in pages:
            filename = "bliss_img" + str(start) + ".png"
            page.save(filename)
            filenames.append(filename)
            start += 1

        self.IMAGES_SAVED = start
        return filenames

    def makeTitlePage(self, title, x, y):
        """
        Returns a title page of given dimensions x and y with the given
        title.

        :param title: str, title name
        :param x: int, x-dimension of output title page
        :param y: int, y-dimension of output title page
        :return: Image, title page
        """
        img = self.makeBlankImg(x, y)
        title_img = self.getWordImg(title, self.font_size)

        img_x = x / 2 - title_img.size[0] / 2
        img_y = y / 3

        img.paste(title_img, (img_x, img_y))
        return img

    def savePdf(self, filename, pages, margins=0):
        """
        Pastes each image file linked to in pages to a PDF.
        ~
        Saves PDF under given filename in this directory.

        Adapted from:
        https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images

        :param filename: str, filename for output PDF
        :param pages: List[str], image filenames to paste in PDF
        :param margins: int, space in margins (in pixels)
        :param delete: bool, whether to delete image files
        :return: None
        """
        pdf = self.getPdf(pages, margins)
        pdf.output(self.FILE_PATH + "/bliss pdfs/" + filename + ".pdf", "F")

    def getPdf(self, pages, margins=0):
        """
        Pastes each image file linked to in pages to a PDF.
        ~
        Returns PDF file.

        Adapted from:
        https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images

        :param pages: List[str], image filenames to paste in PDF
        :param margins: int, space in margins (in pixels)
        :return: None
        """
        width, height = Image.open(pages[0]).size
        new_w, new_h = width + (margins * 2), height + (margins * 2)

        pdf = FPDF(unit="pt", format=[new_w, new_h])
        idx = 0

        for page in pages:
            pdf.add_page()
            pdf.image(page, x=margins, y=margins)

            if len(pages) > 2 and idx > 0 and self.page_nums:
                number = self.getWordImg(str(idx), self.font_size)
                number = self.trim(number)
                num_fn = "num" + str(idx) + ".png"
                number.save(num_fn)
                x = new_w / 2 - number.size[0]
                y = new_h - (margins / 2) - number.size[1]
                pdf.image(num_fn, x=x, y=y)
                os.remove(num_fn)

            os.remove(page)
            idx += 1

        return pdf

    def writePdf(self, text, size=20, margins=0):
        """
        Writes given text to a PDF.
        ~
        Returns PDF file.

        Adapted from:
        https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images

        :param text: str, text to write to PDF
        :param size: int, font size (in pt)
        :param margins: int, space in margins (in pixels)
        :return: None
        """
        # TODO: enable font in other module & write bliss text there
        pdf = FPDF(unit="pt")
        pdf.set_margins(margins, margins)
        pdf.set_auto_page_break(auto=True)
        pdf.add_font(family='Blissymbolics', fname=self.BLISS_FONT)
        pdf.set_font(family='Blissymbolics', size=size)
        pdf.write(txt=text)
        pdf.output(self.FILE_PATH + "/bliss pdfs/" + 'text' + ".pdf", "F")
        pdf.close()
        #return pdf

    def deletePdf(self, filename):
        """
        Deletes PDF with given filename from bliss pdfs folder.

        :param filename: str, filename with .pdf extension
        :return: None
        """
        os.remove(self.FILE_PATH + "/bliss pdfs/" + filename)

    # LANGUAGE PROCESSING
    # ===================
    def unicodize(self, text):
        """
        Returns the given text in unicode.
        ~
        Ensures all text is in unicode for parsing.

        :param text: str, text to return in unicode
        :return: str, text in unicode
        """
        if not isinstance(text, unicode):
            text = text.decode("utf-8")
        return text

    def getWordAndTag(self, word):
        """
        Returns a tuple of the given word and its tag.

        :param word: str, word to tag
        :return: (str, str) tuple, given word and its tag
        """
        if word != "\n":
            if self.language == "English":
                return pos_tag([word], lang=self.lang_code)
            elif self.language in self.PATTERN_LANGS:
                return [tag(word, language=self.lang_code[:2])]
            else:
                return [(word, "")]
        else:
            return [("","")]

    def getWordTag(self, word):
        """
        Returns the given word's tag.

        Caveat: tagging single words outside the context of
        a sentence results in higher errors.

        :param word: str, word to tag
        :return: str, given word's tag
        """
        return self.getWordAndTag(word)[0][1]

    def tokensToTags(self, token_phrase):
        """
        Given a list of strings composing a phrase, returns a list of words'
        part-of-speech tags in that order.

        :param token_phrase: List[str], list of word tokens from a phrase
        :return: List[str], list of word part-to-speech tags
        """
        tagged_phrase = pos_tag(token_phrase,
                                lang=self.lang_code)  # tokens tagged according to word type
        tagged_list = []
        for tup in tagged_phrase:
            tagged_list.append(tup[1])
        return tagged_list

    def getTokenPhrase(self, phrase):
        """
        Returns a list of word tokens in phrase.

        :param phrase: str, text with >=1 words
        :return: List[str], list of word tokens
        """
        return [word for word in word_tokenize(phrase, language=self.language.lower())]

    def getTokenPhrases(self, phrases):
        """
        Returns a list of word tokens in phrases,
        with a newline in between each phrase.

        :param phrases: List[str], phrases to tokenize
        :return: List[str], list of word tokens
        """
        token_phrases = []
        for phrase in phrases:
            token_phrases.extend(self.getTokenPhrase(phrase))
            token_phrases.append("\n")
        return token_phrases

    def isNoun(self, word):
        """
        Returns True if word is a noun, False otherwise.

        :param word: str, word to test whether a noun
        :return: bool, whether given word is a noun
        """
        tag = self.getWordTag(word)
        return tag[0:2] == "NN"

    def isPluralNoun(self, word):
        """
        Returns True if word is a plural noun, False otherwise.

        :param word: str, word to test whether a plural noun
        :return: bool, whether given word is a plural noun
        """
        return self.getWordTag(word) == "NNS"

    def isVerb(self, word):
        """
        Returns True if word is a verb, False otherwise.

        :param word: str, word to test whether a verb
        :return: bool, whether given word is a verb
        """
        tag = self.getWordTag(word)
        return tag[0:2] == "VB"

    def isAdj(self, word):
        """
        Returns True if word is an adjective, False otherwise.

        :param word: str, word to test whether an adjective
        :return: bool, whether given word is an adjective
        """
        tag = self.getWordTag(word)
        return tag[0:2] == "JJ"

    def isPunctuation(self, word):
        """
        Returns True if the input is a punctuation mark.

        :param word: str, word to see if punctuation
        :return: bool, whether word is punctuation
        """
        return word in self.PUNCTUATION

    def isStartingPunct(self, word):
        """
        Returns True if the input is starting punctuation.

        :param word: str, word to see if starting punctuation
        :return: bool, whether word is starting punctuation
        """
        return word in self.STARTING_PUNCT

    def isEndingPunct(self, word):
        """
        Returns True if the input is ending punctuation.

        :param word: str, word to see if ending punctuation
        :return: bool, whether word is ending punctuation
        """
        return word in self.ENDING_PUNCT

    def isNewline(self, word):
        """
        Returns True if the input is a newline.

        :param word: str, word to see if newline
        :return: bool, whether word is newline
        """
        return word == "\n"

    def getWordPOS(self, word):
        """
        Returns the given word's part of speech, abbreviated as a
        single letter.

        POS constants (from WordNet.py):
            ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'

        :param word: str, word to determine pos
        :return: str, letter representing input word's pos
        """
        if self.isNoun(word):
            return "n"
        elif self.isVerb(word):
            return "v"
        elif self.isAdj(word):
            return "a"
        elif self.getWordTag(word)[0:2] == "RB":
            return "r"
        # elif self.getWordTag(word) == "JJS":
        #    return "s"
        else:
            return "n"

    def isChosenPOS(self, pos):
        """
        Returns True if words with the given part of
        speech should be translated, False otherwise.

        :param pos: str, part-of-speech tag
        :return: bool, whether to translate pos
        """
        if self.lang_code != "eng":
            return True
        else:
            return pos in self.CHOSEN_POS

    def getSingular(self, word):
        """
        Returns the singular form of the given word
        in this BlissTranslator's set language.
        ~
        If word cannot be singularized for this
        language, this method returns the input.

        :param word: str, word to singularize
        :return: str, singularized input
        """
        if self.language == "English":
            return en.singularize(word)
        elif self.language == "Spanish":
            return es.singularize(word)
        elif self.language == "German":
            return de.singularize(word)
        elif self.language == "French":
            return fr.singularize(word)
        elif self.language == "Italian":
            return it.singularize(word)
        elif self.language == "Dutch":
            return nl.singularize(word)
        else:
            return word

    def getInfinitive(self, verb):
        """
        Returns the infinitive of the given verb
        in this BlissTranslator's set language.
        ~
        If no infinitive can be found in set language,
        this method returns the input.

        :param verb: str, verb
        :return: str, lemma of verb
        """
        if self.language == "English":
            return en.lemma(verb)
        elif self.language == "Spanish":
            return es.lemma(verb)
        elif self.language == "German":
            return de.lemma(verb)
        elif self.language == "French":
            return fr.lemma(verb)
        elif self.language == "Italian":
            return it.lemma(verb)
        elif self.language == "Dutch":
            return nl.lemma(verb)
        else:
            return verb

    def getPredicative(self, adj):
        """
        Returns the base form of the given adjective
        in this BlissTranslator's set language.
        ~
        If no base form can be found in set language,
        this method returns the input.

        e.g. well   -> good
             belles -> beau

        :param adj: str, adjective
        :return: str, base form of input adj
        """
        if self.language == "English":
            return en.predicative(adj)
        elif self.language == "Spanish":
            return es.predicative(adj)
        elif self.language == "German":
            return de.predicative(adj)
        elif self.language == "French":
            return fr.predicative(adj)
        elif self.language == "Italian":
            return it.predicative(adj)
        elif self.language == "Dutch":
            return nl.predicative(adj)
        else:
            return adj

    def getLexeme(self, word):
        """
        Retrieves the given word's lexeme,
        i.e., the word in dictionary entry form.

        e.g. getLexeme(ran) -> "run"
             getLexeme(puppies) -> "puppy"

        Note: if a lexeme for the given word cannot
        be found, this method returns the input.

        :param word: str, word to convert to lexeme
        :return: str, lexeme of input word
        """
        if word in self.bliss_dict:
            return word
        elif self.language == "Polish":
            try:
                self.polish_lexicon[word]
            except KeyError:
                return word
            else:
                return self.polish_lexicon[word]
        else:
            if self.getSingular(word) in self.bliss_dict:
                return self.getSingular(word)
            elif self.getInfinitive(word) in self.bliss_dict:
                return self.getInfinitive(word)
            elif self.getPredicative(word) in self.bliss_dict:
                return self.getPredicative(word)
            else:
                return word

    def isTranslatable(self, word):
        """
        Returns True if word or word lexeme can be translated to
        Blissymbols, False otherwise.

        :param word: str, word to test whether translatable
        :return: bool, whether given word is translatable
        """
        return self.getLexeme(word) in self.bliss_dict

    def isSynonymTranslatable(self, word):
        """
        Given a word, returns True if any of its synonyms
        are translatable.

        :param word: str, word to generate synonyms
        :return: bool, whether word synonyms are translatable
        """
        synonym = self.translateUntranslatable(word)
        return synonym != ""

    def canBeTranslated(self, word):
        """
        Returns True if given word or any of its synonyms
        are translatable, False otherwise.

        :param word: str, word to see if can be translated
        :return: bool, whether word can be translated
        """
        return self.isTranslatable(word) or self.isSynonymTranslatable(word)

    def shouldBeTranslated(self, word, word_tag, lexeme):
        """
        Returns True if this word should be translated
        (according to this BlissTranslator's language
        preferences), False otherwise.

        :param word: str, word whether to translate
        :param word_tag: str, word's pos tag (see PARTS_OF_SPEECH)
        :param lexeme: str, input word's lexeme
        :return: bool, whether this word should be translated
        """
        return (not self.isPunctuation(word)) and \
               self.isChosenPOS(word_tag) and \
               self.canBeTranslated(lexeme)

    def translateNow(self, lexeme):
        """
        Returns True if words with given lexeme should be
        translated now, False if later/never.

        :param lexeme: str, lexeme (corresponds to multiple word forms)
        :return: bool, whether to translate given lexeme now
        """
        return self.fast_translate or self.isSeen(lexeme)

    def bestWordChoice(self, word):
        """
        Determines best guess for correct Bliss translation of given word.
        Returns an integer representing the index of best guess in word's
        list of defns.

        :param word: str, word to determine best translation of
        :return: int, index of best translation of given word
        """
        defns = self.bliss_dict[word]
        idx = 0

        for defn in defns:
            in_parens = False
            paren_phrase = []

            for char in defn[::-1]:
                if char == "(":
                    in_parens = False
                if in_parens:
                    paren_phrase.insert(0, char)
                if char == ")":
                    in_parens = True

            try:
                paren_phrase[0]
            except IndexError:
                return idx
            else:
                paren_phrase = "".join(paren_phrase)
                if paren_phrase != "feminine" and paren_phrase != "masculine":
                    return idx
            finally:
                idx += 1
        else:
            return 0

    def chooseDefn(self, word):
        """
        Returns an integer representing the index of a word definition
        in given word's list of defns.
        ~
        If list of definitions contains only 1 item, returns 0.

        :param word: str, a word to choose a definition for
        :return: int, index of chosen definition for given word
        """
        if word not in self.defns_chosen.keys():
            defns = self.bliss_dict[word]

            if type(defns) == list:
                idx = 1
                print("The word '" + word + "' has multiple definitions:\n")

                for defn in defns:
                    print("Definition " + str(idx) + ": " + defn[:-4] + "\n")
                    idx += 1

                choice = input("Which of these definitions is most appropriate? ")
                print("\n")

                try:
                    defns[choice]
                except IndexError:
                    choice = 0
                else:
                    choice -= 1  # subtract 1 from choice for 0-based indexing
                    self.defns_chosen[word] = choice
                return choice
            else:
                return 0
        else:
            return self.defns_chosen[word]

    def getWordSynsets(self, word):
        """
        Returns a list of WordNet synsets for the given word.

        WordNet lookup link here:
        http://wordnetweb.princeton.edu/perl/webwn?s=&sub=Search+WordNet

        :param lexeme: str, a word to lookup in WordNet
        :return: List[Synset], the word's synsets
        """
        pos = self.getWordPOS(word)

        synsets = wordnet.synsets(word, pos, lang=self.lang_code)

        if len(synsets) == 0:
            synsets = wordnet.synsets(word, lang=self.lang_code)

        return synsets

    def getSynsetLemmas(self, synset):
        """
        Given a synset, returns a list of its lemma names.

        :param synset: Synset, WordNet synset
        :return: List[str], WordNet lemma names
        """
        return synset.lemma_names(lang=self.lang_code)

    def getSynsetsLemmas(self, synsets):
        """
        Given a list of WordNet synsets, returns a list
        of all of their lemma names.

        :param synsets: List[Synset], synsets
        :return: List[str], lemmas for all synsets
        """
        lemmas = []
        for synset in synsets:
            lemmas.extend(self.getSynsetLemmas(synset))
        return lemmas

    def getWordSynsetsLemmas(self, word):
        """
        Returns all lemma names in all synsets
        associated with given word.

        :param word: str, a word to lookup in WordNet
        :return: List[str], all this word's synsets' lemmas
        """
        return self.getSynsetsLemmas(self.getWordSynsets(word))

    def translateSynsets(self, synsets):
        """
        Given a list of synsets, attempts to translate each
        synset into Blissymbols.
        ~
        If a synonym is translatable to Blissymbols, return
        that synonym. Otherwise, return the empty string.

        :param synsets: List[Synset], a root word and its synonyms
        :return: str, first word in synset translatable to Blissymbols
        """
        for synset in synsets:
            for lemma in self.getSynsetLemmas(synset):
                if self.isTranslatable(lemma):
                    return self.getLexeme(lemma)
        return ""

    def translateUntranslatable(self, word):
        """
        Attempts to translate the given word's synonyms to
        Blissymbols.
        ~
        If a synonym can be translated, this method returns
        that synonym. Otherwise, this method returns the
        input word.

        :param word: str, word to translate to Blissymbols
        :return: str, translatable synonym of given word
        """
        return self.translateSynsets(self.getWordSynsets(word))

    def getSynsetDefn(self, synset):
        """
        Returns this Synset's definition.

        :param synset: Synset, a WordNet synset
        :return: str, the given synset's definition
        """
        return synset.definition()

    def getWordDefn(self, word):
        """
        Returns the first possible definition for the
        given word.

        :param word: str, the word to define
        :return: str, the word's first possible definition
        """
        return self.getSynsetDefn(self.getWordSynsets(word)[0])

    def getWordDefns(self, word, single=False):
        """
        Returns a list of possible definitions for the
        given word.
        ~
        If single is True, then this method will
        return the first definition reached.

        :param word: str, the word to define
        :param single: bool, whether to return the first
            definition reached
        :return: List[str], the word's possible definitions
        """
        defns = []
        synsets = self.getWordSynsets(word)

        for synset in synsets:
            defns.append(self.getSynsetDefn(synset))
            if single:
                return defns

        return defns

    def getWordAtIndex(self, token_phrase, idx):
        """
        A try-catch block for returning the word
        token in token_phrase at specified idx.
        ~
        If index cannot be reached, this method returns
        the empty string.

        :param token_phrase: List[str], word tokens
        :param idx: int, index to access in token_phrase
        :return: str, word token at specified idx
        """
        try:
            token_phrase[idx]
        except IndexError:
            return ""
        else:
            return token_phrase[idx]

    def getTitle(self, title, phrase):
        """
        Returns a valid title for the given phrase.
        ~
        If input title is None, this method returns the first 20
        alphabetic characters and/or spaces in phrase as a working title.
        Otherwise, this method returns the input title's valid characters.

        :param title: None or str, user-selected title
        :param phrase: str, phrase being titled
        :return: str, valid title for given phrase
        """
        if title is None:
            title = phrase[:20]
        return title

    def parsePlaintext(self, filename):
        """
        Parses plaintext file with given filename and returns a string representing
        its contents.

        :param filename: str, filename of text file
        :return: str, text file's contents
        """
        contents = []
        slash = "/" if filename[0] != "/" else ""

        with open(self.FILE_PATH + slash + filename, "rb") as text:
            for line in text:
                contents.append(line)

        return "".join(contents)

    # TRANSLATOR
    # ==========
    def translate(self, phrase, title=None, title_page=False, img_w=816, img_h=1056):
        """
        Translates input phrase to Blissymbols according to this
        BlissTranslator's POS and language preferences.
        ~
        Saves translation to a PDF file in this directory's
        bliss pdfs folder with the given title, or otherwise
        titled after the given phrase's first 20 characters.
        ~
        Default image size is 816x1056px (standard PDF page).

        :param phrase: str, text in BlissTranslator's native language
        :param title: None or str, desired title for output PDF
        :param img_w: int, desired width of PDF images (in pixels)
        :param img_h: int, desired height of PDF images (in pixels)
        :param title_page: bool, whether to create title page
        :return: None, saves PDF with translation to bliss pdfs folder
        """
        # TODO: refactor translate() & drawAlphabet() for less repetition
        # TODO: refactor tokenizing to allow translating compound words & hyphenates
        title, phrase = self.unicodize(title), self.unicodize(phrase)
        phrase = phrase.replace("-", " - ")
        phrases = phrase.split("\n")  # split input by newlines
        token_phrases = self.getTokenPhrases(phrases)
        tagged_list = self.tokensToTags(token_phrases)
        raw_phrase = [word.lower() for word in token_phrases]

        pages = []  # translated images to convert to PDF
        if title_page:
            title_pg = self.makeTitlePage(title, img_w, img_h)
            pages.append(title_pg)

        bg = self.makeBlankImg(img_w, img_h)
        indent = self.font_size
        line_no = 0
        idx = 0

        for word in raw_phrase:
            if word in self.WHITESPACE:
                img = self.makeBlankImg(0, 0)
            else:
                lexeme = self.getLexeme(word)
                word_token = token_phrases[idx]
                word_tag = tagged_list[idx]

                if not self.shouldBeTranslated(word, word_tag, lexeme):
                    # if word can't be translated to Blissymbols,
                    # then render text
                    img = self.getWordImg(word_token, self.font_size)

                elif not self.translateNow(lexeme):
                    # if we don't want to translate this word yet,
                    # then render text
                    img = self.getWordImg(word_token, self.font_size)
                    self.addSeen(lexeme)

                else:
                    if self.isTranslatable(lexeme):
                        new_lexeme = lexeme
                    else:
                        new_lexeme = self.getLexeme(self.translateUntranslatable(word))

                    try:
                        self.getSubbedBlissImg(new_lexeme, img_w/2, self.image_heights)
                    except SystemError:
                        img = self.getWordImg(word_token, self.font_size)
                    else:
                        if self.isChanged(lexeme) and not self.sub_all:
                            img = self.getSubbedBlissImg(new_lexeme, img_w/2, self.image_heights, subs=False)
                        else:
                            # adds subtitles to new words
                            img = self.getSubbedBlissImg(word, img_w/2, self.image_heights, subs=True)
                            self.addChanged(lexeme)

                        if self.isPluralNoun(word):
                            # affixes plural Blissymbol to plural nouns
                            img = self.getPluralImg(img)

            space = self.getSpaceSize()
            x_inc = indent + self.getWordWidth(img)
            y_inc = self.font_size * 3

            this_word = raw_phrase[idx]
            next_word1 = self.getWordAtIndex(raw_phrase, idx + 1)
            next_word2 = self.getWordAtIndex(raw_phrase, idx + 2)

            # TODO: design a method to handle spacing between irregular characters
            if next_word1 == "n't" or next_word1 == "'s":
                space = self.getMinSpace()
            elif self.isEndingPunct(this_word) and self.isEndingPunct(next_word1):
                space = self.getMinSpace()
            elif self.isStartingPunct(next_word1) or self.isEndingPunct(this_word):
                space = self.getSpaceSize()
            elif self.isEndingPunct(next_word1) or self.isStartingPunct(this_word):
                space = self.getMinSpace()

            # TODO: design a method to handle indentation/linenumbers
            if x_inc > img_w:
                indent = 0
                line_no += 1
            elif self.isEndingPunct(next_word2) or self.isStartingPunct(next_word1):
                if (x_inc + self.getWordWidth(next_word1) + space * 2 + self.getWordWidth(next_word2)) > img_w:
                    # don't let punctuation trail onto next line alone
                    indent = 0
                    line_no += 1
            elif this_word == "\n":
                indent = self.font_size
                line_no += 1

            if (line_no + 1) * y_inc > img_h:
                # if the next line would go beyond the image,
                # store the current page and go onto a new one
                pages.insert(0, bg)
                bg = self.makeBlankImg(img_w, img_h)
                line_no = 0

            # TODO: modify paste to work with vector bliss files (for aesthetic resizing)
            bg.paste(img, (indent, self.incLine(line_no, y_inc)))
            indent += self.getWordWidth(img) + space
            idx += 1

        pages.insert(0, bg)
        self.savePdf(title, self.saveImages(pages[::-1]), margins=50)
        self.initSeenChanged()

    def translateFile(self, filename, title=None, img_w=816, img_h=1056):
        """
        Parses a plaintext file in this directory with given filename
        to a string, then passes the result as a phrase to translate().

        :param filename: str, .txt file in this directory
        :param title: None or str, desired title for output PDF
        :param img_w: int, desired width of PDF images (in pixels)
        :param img_h: int, desired height of PDF images (in pixels)
        :return: None
        """
        phrase = self.parsePlaintext(filename)
        self.translate(phrase, title, img_w, img_h)