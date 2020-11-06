# -*- coding: utf-8 -*-
"""
PARSE_LEXICA:

    Used for parsing Blissymbols to dictionaries.

    Throughout Blisscribe, "lemma" is meant to be the dictionary
    entry of a word, while "lexeme" is meant to be any form of a
    word.  All lemmas are lexemes, but only 1 in a set of lexemes
    is chosen as the lemma.
    e.g. "dog": lexeme and lemma
         "dogs": lexeme but not lemma

    Alphabetical list of part-of-speech tags used in the
    Penn Treebank Project:

    Number  Tag     Description
    1.      CC      Coordinating conjunction
    2.      CD	    Cardinal number
    3.	    DT	    Determiner
    4.	    EX	    Existential there
    5.	    FW	    Foreign word
    6.	    IN	    Preposition or subordinating conjunction
    7.	    JJ	    Adjective
    8.	    JJR	    Adjective, comparative
    9.	    JJS	    Adjective, superlative
    10.	    LS	    List item marker
    11.	    MD	    Modal
    12.	    NN	    Noun, singular or mass
    13.	    NNS	    Noun, plural
    14.	    NNP	    Proper noun, singular
    15.	    NNPS	Proper noun, plural
    16.	    PDT	    Predeterminer
    17.	    POS	    Possessive ending
    18.	    PRP	    Personal pronoun
    19.	    PRP$	Possessive pronoun
    20.	    RB	    Adverb
    21.	    RBR	    Adverb, comparative
    22.	    RBS	    Adverb, superlative
    23.	    RP	    Particle
    24.	    SYM	    Symbol
    25.	    TO	    to
    26.	    UH	    Interjection
    27.	    VB	    Verb, base form
    28.	    VBD	    Verb, past tense
    29.	    VBG	    Verb, gerund or present participle
    30.	    VBN	    Verb, past participle
    31.	    VBP	    Verb, non-3rd person singular present
    32.	    VBZ	    Verb, 3rd person singular present
    33.	    WDT	    Wh-determiner
    34.	    WP	    Wh-pronoun
    35.	    WP$	    Possessive wh-pronoun
    36.	    WRB	    Wh-adverb
"""
import os, sys

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(PATH)
import json
import pprint
from imports import safe_import

safe_import("blissymbol")
safe_import("bliss_lexicon")
safe_import("resources")
from blissymbol import Blissymbol, NEW_BLISSYMBOLS
from bliss_lexicon import BlissLexicon
from resources.data.blissnets import BLISSNET, BCI_BLISSNET, ALL_BLISSYMBOLS


class LexiconParser:
    RESOURCE_PATH = PATH + "/resources/"
    DATA_PATH = RESOURCE_PATH + "data/"
    BLISSCHARS_PATH = DATA_PATH + "blissymbols_gh_pages/blissdata_chars.json"
    BLISSWORDS_PATH = DATA_PATH + "blissymbols_gh_pages/blissdata_words.json"
    WORDNET_PATH = RESOURCE_PATH + "wordnet/"
    LEXICA_PATH = RESOURCE_PATH + "lexica/"
    LEXICON_COLS = [
        "BCI-AV#",
        "English",
        "POS",
        "Derivation - explanation",
        "BCI-AV#",
        "Swedish",
        "BCI-AV#",
        "Norwegian",
        "BCI-AV#",
        "Finnish",
        "BCI-AV#",
        "Hungarian",
        "BCI-AV#",
        "German",
        "BCI-AV#",
        "Dutch",
        "BCI-AV#",
        "Afrikaans",
        "BCI-AV#",
        "Russian",
        "BCI-AV#",
        "Latvian",
        "BCI-AV#",
        "Polish",
        "BCI-AV#",
        "French",
        "BCI-AV#",
        "Spanish",
        "BCI-AV#",
        "Portuguese",
        "BCI-AV#",
        "Italian",
        "BCI-AV#",
        "Danish",
    ]
    BLISS_LANGS = {
        "English",
        "Swedish",
        "Norwegian",
        "Finnish",
        "Hungarian",
        "German",
        "Dutch",
        "Afrikaans",
        "Russian",
        "Latvian",
        "Polish",
        "French",
        "Spanish",
        "Portuguese",
        "Italian",
        "Danish",
    }

    def __init__(self, translator):
        self.translator = translator
        self.bliss_derivations = self.load_bliss_derivations()
        self.blissymbols = BlissLexicon(self.translator).blissymbols

    def check_blissymbols(self):
        for b in self.blissymbols:
            deriv = self.official_derivation(b.bliss_name)
            print("blissymbol", b.bliss_name, "has official derivation", deriv, end=" ")
            if deriv is not None:
                b.derivation = deriv
            print("and derivation", b.derivation)
        print(self.blissymbols)

    @property
    def blissnet(self):
        return BLISSNET

    @property
    def bci_blissnet(self):
        return BCI_BLISSNET

    # JSON
    # ====
    def write_python(self, data, filename, obj_name):
        with open(
            self.DATA_PATH + filename + ".py", mode="w", encoding="utf-8"
        ) as pyfile:
            pyfile.write(obj_name + " = ")
            pyfile.write(pprint.pformat(data, indent=1))

    def dump_json(self, data, filename, **kwargs):
        """
        Dumps data (prettily) to filename JSON.

        :param data: X, data to dump to JSON
        :param filename: str, name of .json file to dump to
        :return: None
        """
        path = self.DATA_PATH + filename + ".json"
        indent = kwargs.setdefault("indent", 1)
        sort_keys = kwargs.setdefault("sort_keys", True)
        ascii = kwargs.setdefault("ensure_ascii", False)
        json.dump(
            data,
            open(path, "w", encoding="utf-8"),
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=ascii,
        )

    def load_json(self, filename):
        """
        Returns the official Blissymbols lexicon.

        :param filename: str, name of .json file to fetch
        :return: X, content of given .json file
        """
        return json.load(open(self.DATA_PATH + filename + ".json", encoding="utf-8"))

    # BLISS DATA
    # ==========
    #   1)  All Blissymbols
    #   2)  BCI-Blissname Map
    #   3)  BCI Blissnet
    #   4)  Bliss Derivations
    #   5)  Bliss Unicode En-/Decoding
    #   6)  Bliss Lexicon
    #   7)  Bliss Unicode
    #   8)  Blissnet
    #   9)  Blisswordnet
    #   10) WordNet 3.0-to-3.1 Map

    # ALL BLISSYMBOLS
    # ---------------
    def load_all_blissymbols(self):
        """
        Returns a list of dictionaries, each of which represents a
        Blissymbol from the official Blissymbols lexicon.

        :return: List[dict(str, X)], where...
            key (str) - Blissymbol's attribute
            val (X) - attribute's value
        """
        return ALL_BLISSYMBOLS

    def fresh_all_blissymbols(self):
        blissymbols = self.load_all_blissymbols()
        for bs in blissymbols:
            bs["derivation"] = self.official_derivation(bs["name"])
        blissymbols = {self.dict_to_blissymbol(bs) for bs in blissymbols}
        if None in blissymbols:
            blissymbols.remove(None)
        self.refresh_bliss_lexicon(blissymbols)
        return blissymbols

    def official_derivation(self, blissname):
        print("FINDING DERIVATION FOR", blissname)
        deriv = self.bliss_derivations.get(blissname, None)
        if deriv is not None:
            print(blissname, "derivation is: ", " + ".join(deriv))
        return deriv

    def refresh_bliss_lexicon(self, blissymbols=None):
        if blissymbols is None:
            self.check_blissymbols()
            blissymbols = self.blissymbols
        blissymbols = sorted(blissymbols, key=lambda b: b.bci_num)
        with open(PATH + "/bliss_lexicon.py", mode="w") as bliss_file:
            bliss_file.write(
                "import os, sys\n"
                "sys.path.append(os.path.realpath(__file__))\n"
                "from blissymbol import Blissymbol\n\n\n"
                "class BlissLexicon:\n\n\t"
                "def __init__(self, translator):\n\t\t"
                "self.translator = translator\n\t\t"
                "self.blissymbols = {\n\t\t\t".replace("\t", "    ")
            )
            for i in range(len(blissymbols)):
                blissymbol = blissymbols[i]
                bliss_str = str(blissymbol)
                bliss_file.write(bliss_str)
                if i < len(blissymbols) - 1:
                    bliss_file.write(",\n\t\t\t".replace("\t", "    "))
            bliss_file.write("\n\t\t}".replace("\t", "    "))

    # BCI-BLISSNAME MAP
    # -----------------
    def load_bci_blissname_map(self):
        """
        Returns a dict from BCI-AV ID numbers to their
        corresponding Blissymbol's name.
        ~
        N.B. Blissymbol names are a comma-separated string of
             1 or more English words.

        :return: dict, where...
            key (int) - BCI-AV number for a Blissymbol
            val (str) - Blissymbol's name
        """
        return self.load_json("bci_blissname_map")

    def fresh_bci_blissname_map(self):
        """
        Returns a dict mapping BCI-AV numbers to Blissymbol
        names and dumps it to bci-av_map_blissnames JSON.
        ~
        N.B. Blissymbol names are a comma-separated string of
             1 or more English words.

        :return: dict(int, str), where...
            key (int) - BCI-AV number for a Blissymbol
            val (str) - Blissymbol's name
        """
        bliss_dict = self.load_all_blissymbols()
        bci_mapping = {}

        for entry in bliss_dict:
            bci_av = int(entry["BCI-AV"])
            name = entry["name"]
            bci_mapping[bci_av] = name

        self.dump_json(bci_mapping, "bci-av_mapping")
        return bci_mapping

    # BCI BLISSNET
    # ------------
    def fresh_bci_blissnet(self):
        """
        Returns a dict mapping BCI-IV Blissymbol IDs
        to a list of WordNet synset strings, and
        dumps it to bci_blissnet JSON.

        :return: dict(int, list), where...
            key (int) - BCI-AV number
            val (List[str]) - strings for WordNet synsets
        """
        blissnet = self.translator.blissnet

        bci_map = self.load_bci_blissname_map()
        bliss_map = {bliss: bci for bci, bliss in bci_map.items()}
        blissnet_map = self.load_blisswordnet()
        net_bci_map = {}

        for blissword in blissnet_map:
            bci = int(bliss_map[blissword])
            net_bci_map[bci] = blissnet_map[blissword]

        self.dump_json(net_bci_map, "bci_blissnet")
        return net_bci_map

    # BLISS DERIVATIONS
    # -----------------
    def load_bliss_derivations(self):
        """
        Returns a dictionary of Blissymbol derivation strings and
        the list of derivations belonging to that string.
        ~
        Each Blissymbol derivation string consists of 2+ names for
        the Blissymbols it is composed of, or is otherwise atomic.

        :return: dict, where...
            key (str) - Blissymbol derivation string
            val (list) - list of Blissymbol names in this derivation
        """
        worddata = json.load(open(self.BLISSWORDS_PATH))["words"]
        chardata = json.load(open(self.BLISSCHARS_PATH))["chars"]
        worddata.update({c: [c] for c in chardata})
        return worddata

    def fresh_bliss_derivations(self):
        """
        Returns a fresh derivations dictionary for translating
        Blissymbol derivations to words.

        :return: dict, where...
            key (str) - unicode for Blissymbol
            val (List[str]) - Blissymbol names for given unicode
        """
        bliss_derivations = {}

        for blissymbol in self.blissymbols:
            bliss_derivations[blissymbol.bliss_name] = blissymbol.derivations

        self.dump_json(bliss_derivations, "bliss_derivations")
        return bliss_derivations

    # BLISS LEXICON
    # -------------
    def load_bliss_lexicon(self):
        """
        Returns the official Blissymbols lexicon.

        :return: dict, where...
            key (str) - Blissymbol word (in English)
            val (dict) - dict corresponding to Blissymbol word
        """
        return self.load_json("bliss_lexicon")

    def init_bliss_lexicon(self, language):
        """
        Initializes a Blissymbols lexicon in this language.

        :param language: str, desired Blissymbol lexicon language
        :return: dict, where...
            key (str) - word in this language
            val (Set(Blissymbol)) - Blissymbols for word
        """
        bliss_dict = {}

        for blissymbol in self.blissymbols:
            lang_words = blissymbol.get_translation(language)

            for lang_word in lang_words:
                bliss_dict.setdefault(lang_word, set())
                bliss_dict[lang_word].add(blissymbol)

        return bliss_dict

    def refresh_blissymbols(self):
        """
        Refreshes the Blissymbols JSON lexicon to include all new entries in this
        LexiconParser's bliss_dict.

        :return: None
        """
        lexicon = self.translator.bliss_dict("English")
        blissymbols = set()
        for bliss_lst in lexicon.values():
            blissymbols.update(bliss_lst)
        blissymbols = sorted(blissymbols, key=lambda b: b.bci_num)
        bliss_dicts = [b.__dict__() for b in blissymbols]
        if bliss_dicts != self.load_all_blissymbols():
            self.write_python(bliss_dicts, "all_blissymbols", "ALL_BLISSYMBOLS")
            self.refresh_bliss_lexicon(blissymbols)

    # BLISS UNICODE
    # --------------
    def load_bliss_unicode(self):
        """
        Returns a unicode-to-Blissymbol name dictionary.
        ~
        Unicode conforms to suggestions here:
        http://std.dkuug.dk/JTC1/SC2/WG2/docs/n1866.pdf
        ~
        N.B. Blissymbol names are a comma-separated string of
             1 or more English words.

        :return: dict(str, str), where...
            key (str) - unicode for Blissymbol
            val (str) - Blissymbol's name
        """
        return self.load_json("bliss_unicode")

    def fresh_bliss_unicode(self):
        """
        Returns a fresh text-to-unicode dictionary for translating
        words to Blissymbols and dumps it to bliss_unicode JSON.

        :return: dict, where...
            key (str) - unicode for a Blissymbol
            val (List[str]) - Blisswords for this unicode
        """
        blisswords = self.load_json("raw_bliss_unicode")
        lexicon = self.load_bliss_lexicon()
        uni = int("3200", base=16)
        unicodes = {}

        for word in blisswords:
            word = word.lower()
            lookup_word = self.translator.remove_parens(word)
            if lookup_word not in lexicon:
                lookup_word = lookup_word.title()
            hex_uni = "U+" + hex(uni)[-4:]
            unicodes.setdefault(hex_uni, None)

            if lookup_word in lexicon:
                bliss_dicts = lexicon[lookup_word]
                bliss_names = []
                underscored_word = self.translator.underscore(word)
                for bd in bliss_dicts:
                    name = bd["name"]
                    if name[-5:] == "-(to)":
                        continue
                    elif len(bliss_dicts) == 1:
                        bliss_names.append(name)
                    elif word == name:
                        bliss_names.append(name)
                    else:
                        deriv = bd["derivation"]
                        is_atom = deriv[-9:] == "Character"
                        is_char = "Character" in deriv or "[modifi" in deriv

                        if is_atom and underscored_word in name:
                            bliss_names.append(name)
                        elif is_char and underscored_word in name:
                            bliss_names.append(name)
                        else:
                            bliss_name = name.split(",")[0]
                            if underscored_word == bliss_name:
                                bliss_names.append(name)

                if len(bliss_names) != 0:
                    unicodes[hex_uni] = bliss_names[0]
            uni += 1

        self.dump_json(unicodes, "bliss_unicode")
        return unicodes

    def refresh_bliss_unicode(self):
        """
        Overwrites the source unicode-to-Blisswords encoding
        dictionary with this LexiconParser's BlissTranslator's
        bliss_unicode dict.

        :return: None
        """
        unicodes = self.translator.bliss_unicode()
        self.dump_json(unicodes, "bliss_unicode")

    # BLISSNET
    # --------------
    def load_blissnet(self):
        """
        Returns a unicode-to-Synset dictionary from Blissymbols
        to PWN Synsets, where Synsets are loaded as strings.
        ~
        Unicode conforms to suggestions here:
        http://std.dkuug.dk/JTC1/SC2/WG2/docs/n1866.pdf

        :return: dict, where...
            key (str) - unicode for a Blissymbol
            val (List[str]) - Princeton synsets for given unicode
        """
        return self.load_json("blissnet")

    def find_blissnet(self, reverse=False):
        """
        Returns a Blissymbol-to-Synset dictionary for mapping
        Blissymbols to Wordnet.
        ~
        If reverse is True, output dict is Synset-to-Blissymbols instead.

        :param reverse: bool, whether to switch keys & values
        :return: dict, where...
            key (Blissymbol) - Blissymbol with synsets
            val (List[Synset]) - Princeton synsets for given Blissymbol
        """
        blissnet = {
            self.translator.blissword_to_blissymbol(bw): self.translator.strs_synsets(
                self.blissnet[bw]
            )
            for bw in self.blissnet
        }
        if reverse:
            rev_blissnet = {}

            for blissymbol in blissnet:
                synsets = blissnet[blissymbol]
                for synset in synsets:
                    rev_blissnet.setdefault(synset, [])
                    rev_blissnet[synset].append(blissymbol)

            return rev_blissnet
        else:
            return blissnet

    def lookup_bci_blissnet(self, **kwargs):
        """
        Given str synset, returns a Blissymbol name.
        Given int bci_num or blissymbol Blissymbol,
        returns a list of synset strings.
        ~
        If no keyword arg is in bci_blissnet, returns None.

        :keyword synset: str, Synset string to lookup Blissymbol for
        :keyword bci_num: int, BCI-AV# for a Blissymbol to lookup synsets for
        :keyword blissymbol: Blissymbol, blissymbol to lookup synsets for
        :return: str or List[str], BCI-AV# for synset or synsets for BCI-AV#
        """
        synset = kwargs.get("synset", None)
        if synset is not None:
            for bci_num in self.bci_blissnet:
                synsets = self.bci_blissnet[bci_num]
                if synset in synsets:
                    return bci_num
        else:
            bci_num = kwargs.get("bci_num", None)
            if bci_num is None:
                bci_num = kwargs.get("blissymbol").bci_num
            return self.bci_blissnet.get(str(bci_num), None)

    def lookup_blissnet(self, **kwargs):
        """
        Given str synset, returns a Blissymbol name.
        Given str bliss_name or blissymbol Blissymbol,
        returns a list of synset strings.
        ~
        If no keyword arg is in blissnet, returns None.

        :keyword synset: str, Synset string to lookup Blissymbol for
        :keyword bliss_name: str, name for a Blissymbol to lookup synsets for
        :keyword blissymbol: Blissymbol, blissymbol to lookup synsets for
        :return: str or List[str], bliss-name for synset or
                 synset strs for bliss_name/blissymbol
        """
        synset = kwargs.get("synset", None)
        if synset is not None:
            for bliss_name in self.blissnet:
                synsets = self.blissnet[bliss_name]
                if synset in synsets:
                    return bliss_name
            return
        else:
            bliss_name = kwargs.get("bliss_name", None)
            if bliss_name is None:
                bliss_name = kwargs.get("blissymbol").bliss_name
            return self.blissnet.get(bliss_name, None)

    def fresh_blissnet(self):
        """
        Returns a new Blissymbol-to-Synset dict and overwrites
        blissnet.json with it.

        :return: dict, where...
            key (Blissymbol) - Blissymbol with Synsets
            val (List[Synset]) - Synsets for given Blissymbol
        """
        blissnet = {}

        for blissymbol in self.blissymbols:
            synsets = self.translator.blissymbol_to_synsets(blissymbol)
            print(blissymbol, "has synsets:\n\t", synsets, "\n")
            if len(synsets) != 0:
                """
                if len(synsets) >= 3:
                    valids = input("That's " + str(len(synsets)) + " synsets.  "
                                       "Write the indices of the best ones, or N if none exist.\n")
                    if len(valids) != 0:
                        if valids == "N":
                            continue
                        valids = eval("[" + valids.replace(" ", ",") + "]")
                        synsets = [synsets[i-1] for i in valids]
                """
                blissnet.setdefault(blissymbol, synsets[:3])

        self.write_blissnet(blissnet)
        return blissnet

    def write_blissnet(self, blissnet):
        json_blissnet = {}

        for blissymbol in blissnet:
            synsets = blissnet[blissymbol]
            json_blissnet[blissymbol.unicode] = [s.name() for s in synsets]

        self.dump_json(json_blissnet, "blissnet")

    # BLISSWORDNET
    # ------------
    def load_blisswordnet(self):
        """
        Returns a dictionary from Blissymbol names to their
        corresponding PWN Synsets.
        ~
        N.B. Blissymbol names are a comma-separated string of
             1 or more English words.

        :return: dict, where...
            key (str) - name for a Blissymbol
            val (List[str]) - Princeton synsets for given unicode
        """
        return self.load_json("fresh_blisswordnet")

    # WN30-WN31 MAP
    # -------------
    def load_wn30_map_wn31(self):
        """
        Returns a dictionary mapping from WordNet 3.0 to 3.1.
        ~
        Map only contains entry where 3.0 differs from 3.1.

        :return: dict(str, str), where...
            key (str) - WordNet 3.0 synset ID
            val (str) - WordNet 3.1 synset ID
        """
        return self.load_json("wn30map31")

    def fresh_wn30_map_31(self):
        """
        Returns a dict mapping WordNet 3.0 synset ID numbers to
        WordNet 3.1 synset ID numbers, where they differ.
        ~
        Dumps the 3.0-to-3.1 mapping to wn30map31 JSON.
        ~
        N.B. Synset IDs are 8-digit strings of integers.
             Stored as strings since many are preceded by zeroes.

        :return: dict(str, str), where...
            key (str) - WordNet 3.0 synset ID number
            val (str) - corresponding WordNet 3.1 synset ID number
        """
        wn30_wn31_txt = self.load_wn30_map_wn31()
        wn30_wn31_map = {}

        for line in wn30_wn31_txt.readlines():
            if line[0] == "#":  # skip header
                continue
            else:
                line = line.replace("\n", "")
                pos, wn30, wn31 = line.split("\t")
                if wn30 != wn31:  # if wn 3.0 & 3.1 ids differ,
                    wn30_wn31_map[wn30] = wn31  # add to dict

        self.dump_json(wn30_wn31_map, "wn30map31")
        return wn30_wn31_map

    def convert_wn30_31(self, sensekey, wn30_in=True):
        """
        Translates this sensekey from WordNet 3.0 to 3.1
        if wn30_in is True.  Otherwise, translates from WN
        3.1 to 3.0.

        :param sensekey: str, 8-digit sense-key for a synset in WN 3.0/3.1
        :param wn30_in: bool, whether to translate from 3.0 to 3.1
        :return: str, 8-digit sense-key for a synset in WN 3.1/3.0
        """
        wn_map = self.load_wn30_map_wn31()
        if not wn30_in:
            wn_map = {v: k for k, v in wn_map.items()}
        return wn_map.get(sensekey, None)

    # MULTILINGUAL
    # ============
    def parse_lexicon(self, language):
        """
        Parses plaintext file for given language.
        Returns a dict with all words in lexicon
        as keys and corresponding lemma forms as values.
        ~
        Each new lexical entry should be separated by "\n",
        while inflected forms should be separated by ",".
        ~
        Assumes first word on every line is the lemma form
        of all subsequent words on the same line.
        ~
        N.B. The same lemma value will often belong to multiple keys.

        e.g. "kota, kocie, kot" -> {"kota":"kota", "kocie":"kota", "kot":"kota"}

        :param language: str, language of .txt file for lexicon
        :return: dict, where...
            key (str) - inflected form of a word
            val (List[str]) - lemma form(s) of inflected word
        """
        filename = "/resources/lexica/" + language + ".txt"
        lexicon = None

        with open(PATH + filename, "r", encoding="utf-8") as lex:
            if language == "Polish":
                lexicon = self.parse_polish_lexicon(lex)
            elif language == "French":
                lexicon = self.parse_french_lexicon(lex)

        return lexicon

    def parse_french_lexicon(self, lex):
        """
        Parses plaintext file for French lexicon with
        given filename.  Returns a dict with all lexemes
        in French lexicon as keys and corresponding
        lemma forms as values.
        ~
        Each new lexical entry should be separated by "\n",
        while inflected forms should be separated by ",".
        ~
        Assumes second word on every line is the lemma form
        of previous words on the same line.
        ~
        N.B. The same lemma value will often belong to
        multiple lexemes.

        e.g. "grande, grand" -> {"grande":"grand", "grand":"grand"}

        :param lex: List[str], entry in French lexicon
        :return: dict, where...
            key (str) - any lexical form of a word
            val (str) - lemmatized form of lemma
        """
        lexicon = {}

        for line in lex:
            line = str(line).strip("\n")
            if line[-1] == "=":
                lemma = line[:-2]
                lexicon[lemma] = lemma
            else:
                entry = line.split("\t")
                lemma = entry[1]
                lexeme = entry[0]
                lexicon[lexeme] = lemma

        return lexicon

    def parse_polish_lexicon(self, lex):
        """
        Parses plaintext file for Polish lexicon with
        given filename.  Returns a dict with all lexemes
        in Polish lexicon as keys and corresponding
        lemma forms as values.
        ~
        Inflected forms in each lexical entry should be
        separated by ",".
        ~
        Assumes first word on every line is the lemma form
        of following words on the same line.
        ~
        N.B. The same lemma value will often belong to
        multiple lexemes.

        e.g. "kota, kot, kocie" -> {"kota":["kota"], "kot":["kota"], "kocie":["kota"]}

        :param lex: List[str], entry in Polish lexicon
        :return: dict, where...
            key (str) - any lexical form of a word
            val (List[str]) - lemmatized form(s) of lexeme
        """
        lexicon = {}

        for line in lex:
            line = str(line)
            line = line.strip("\n")
            line = line.strip("\r")
            inflexions = line.split(",")
            lemma = inflexions[0]

            for inflexion in inflexions:
                inf = inflexion.strip()
                lexicon.setdefault(inf, [])
                lexicon[inf].append(lemma)

        return lexicon

    # WORDNET
    # =======
    def bliss_wordnet_mapping(
        self,
        bliss_keys=True,
        bliss_attr="gloss",
        wn_attr="name",
        wn_30=True,
        title="bliss_wordnet_mapping",
    ):
        """
        Returns a dict mapping between Blissymbols and WordNet and dumps it to
        /resources/data/[title].json.

        :param bliss_keys: bool, True if Blissymbols should be keys in map, False if values
        :param bliss_attr: str, which
            MUST be one of:
                'gloss' - Blissymbol's gloss, AKA its "bliss-name" (e.g. "cat,feline_(animal),felid")
                'unicode' - Blissymbol's unicode representation (e.g. "U+349b")
                'number' - Blissymbol's BCI-AV# (e.g. 12383)
        :param wn_attr: str,
            MUST be one of:
                'sense-key' - Synset's gloss, AKA its "bliss-name" (e.g. "cat,feline_(animal),felid")
                'name' - Synset's first lemma, pos, and sense number (e.g. "cat.n.01")
                'lemma_names' - Synset's lemmas' names (e.g. ["cat", "feline", "felid"])
        :param wn_30: bool,
        :param title: str, name of JSON file to dump mapping to
        :return: dict(X, Y), Blissymbols mapped to Synsets OR Synsets mapped to Blissymbols
        """

        def transform_bliss(bs):
            if bliss_attr == "unicode":
                return bs.unicode
            elif bliss_attr == "number":
                return bs.bci_num
            else:
                try:
                    return getattr(bs, bliss_attr)
                except AttributeError:
                    return bs.bliss_name

        def transform_synset(s):
            if wn_attr == "sense-key":
                self.translator.synset_id()
                synset_30 = str(s.offset()).zfill(8)
                if not wn_30:
                    return self.convert_wn30_31(synset_30, wn30_in=True)
                else:
                    return synset_30
            else:
                try:
                    return getattr(s, wn_attr)
                except AttributeError:
                    return s.name()

        bliss_wn_map = {}

        for blissymbol in self.blissymbols:
            synsets = self.translator.blissymbol_to_synsets(blissymbol)
            if len(synsets) != 0:
                trans_bliss = transform_bliss(blissymbol)
                trans_synsets = [transform_synset(ss) for ss in synsets]
                if bliss_keys:
                    bliss_wn_map[trans_bliss] = trans_synsets
                else:
                    for trans_synset in trans_synsets:
                        bliss_wn_map.setdefault(trans_synset, []).append(trans_bliss)

        self.dump_json(bliss_wn_map, filename=title)
        return bliss_wn_map

    def blissnum_sensekey_mapping(self, wn_version=3.0):
        """
        Returns a dict mapping Blissymbol BCI_AV# to WordNet 3.0 or 3.1 synset sense-key,
        and dumps it to bci_blissnet_3.0/3.1 JSON.
        ~
        Synset id # corresponds to WordNet version specified in wn_version (either 3.0 or 3.1).
        ~
        N.B. WordNet sense-keys are 8-digit strings (can start with 0) of numbers

        :param wn_version: float, version of WordNet to use (3.0 or 3.1)
        :return: dict(int, list), where...
            key (int) - BCI_AV# for a Blissymbol
            val (List[str]) - synset sense-key for this Blissymbol
        """
        bci_blissnet = self.bci_blissnet
        blissnet_30 = {}

        for bci in bci_blissnet:
            synset_strs = bci_blissnet[bci]
            synset_30_ids = [
                str(self.translator.str_synset_id(s))[1:] for s in synset_strs
            ]
            blissnet_30[int(bci)] = synset_30_ids

        if wn_version == 3.0:
            self.dump_json(blissnet_30, "bci_blissnet_3.0")
            return blissnet_30
        elif wn_version == 3.1:
            wn30_map_31 = self.load_wn30_map_wn31()
            blissnet_31 = {
                int(bci): [wn30_map_31.get(id30, id30) for id30 in ids30]
                for bci, ids30 in blissnet_30.items()
            }
            self.dump_json(blissnet_31, "bci_blissnet_3.1")
            return blissnet_31

    def synset_sensekey_mapping(self):
        """
        Maps WordNet 3.0 synsets to sense-keys.

        :return: dict(str, str), where...
            key (str) - WN synset, e.g. "dog.n.1"
            val (str) - 8-digit WN sense-key, e.g. "02084071"
        """
        from nltk.corpus import wordnet

        synsets = wordnet.all_synsets()
        del wordnet
        mapping = {}

        for synset in synsets:
            str_synset = synset.name()
            sense_key = str(synset.offset()).zfill(8)
            mapping[str_synset] = sense_key

        self.dump_json(mapping, "synset_sense-key_mapping")
        return mapping

    def bliss_dict_to_wordnet(self, bliss_dict):
        """
        Returns a dictionary of Blissymbol word keys and synsets
        from this bliss_dict.
        ~
        N.B. Output will be most accurate with a multilingual
        Bliss dictionary.

        :param bliss_dict: dict, where...
            key (str) - Blissymbol word in English
            val (List[Blissymbol]) - corresponding Blissymbols with
                translations in all languages
        :return: dict, where...
            key (str) - Blissymbol's unicode representation
            val (List[Synset]) - synsets associated with Blissymbol
        """
        wordnet = {}

        for word in bliss_dict:
            for blissymbol in bliss_dict[word]:
                uni = blissymbol.unicode
                synsets = blissymbol.synsets
                wordnet[uni] = synsets

        return wordnet

    def get_tab_file(self, lang_code):
        """
        Retrieves a multilingual WordNet tab file for the
        given language.
        ~
        If no such tab file exists, returns None.

        :param lang_code: str, 3-character ISO language code
        :return: tab file, WordNet file for given language
        """
        try:
            tab_path = PATH + "/resources/omw_tabs/" + "wn-cldr-" + lang_code + ".tab"
            return open(tab_path, encoding="utf-8")
        except IOError:
            raise IOError("Blisscribe doesn't support this language yet... oops!")

    # BLISS MANIPULATION
    # ==================
    def make_blissymbol(self):
        """
        Prompts user for new Blissymbol entry information.

        :return: Blissymbol, represents 1 Bliss lexical entry
        """
        bliss_name = input("What do you call your new Blissymbol? ")
        print("Which part of speech is this? ")
        code = Blissymbol.POS_COLOUR_CODE

        for pos in code:
            print(str(pos) + ":\t" + str(code[pos]))

        pos = input("")
        print("Which atomic Blissymbols is this made of? ")
        derivations = input("Separate them by commas: ")
        derivations = derivations.split(",")
        derivs = ""
        derivs += "("

        for idx in range(0, len(derivations)):
            derivs += derivations[idx]
            if idx == len(derivations) - 1:
                derivs += ")"
            else:
                derivs += " + "

        translations = {}

        for language in self.BLISS_LANGS:
            print("What is/are the translation(s) in " + language + "? ")

            try:
                translation = input("Separate by commas if necessary: ")
            except SyntaxError:
                continue
            else:
                translation = translation

            translations.setdefault(language, [])
            translations[language].append(translation)

        blissymbol = Blissymbol(
            bliss_name=bliss_name,
            pos=pos,
            derivation=derivs,
            translations=translations,
            translator=self.translator,
            num=0,
        )
        return blissymbol

    def dict_to_blissymbol(self, d):
        """
        Returns this dict, d, as a Blissymbol.
        ~
        This method assumes d has keys named
        "name", "pos", "derivation", and "translations",
        and initializes a Blissymbol with its fields corresponding
        to these keys.

        :param d: dict, dictionary to turn into Blissymbol
        :return: Blissymbol, d as a Blissymbol
        """
        name = d["name"]

        if name[-7:-1] != "ercase" and name[-4:-1] != "OLD":
            blissymbol = Blissymbol(
                name,
                d["pos"],
                d.get("derivation", ""),
                d.get("translations", {}),
                self.translator,
                num=d["BCI-AV"],
            )
            return blissymbol
