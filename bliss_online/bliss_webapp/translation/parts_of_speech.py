# coding: utf-8
"""
PARTS_OF_SPEECH:

    Holds parts-of-speech and language codes for Blisscribe.
"""

# WORDNET
# -------
PARTS_OF_SPEECH = {  # Penn Treebank parts of speech, used by Wordnet
    "CC": "Coordinating conjunction",
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
    "WRB": "Wh-adverb",
}
WORDNET_SUPPORTED_LANGS = {
    "eng",
    "als",
    "arb",
    "bul",
    "cat",
    "cmn",
    "dan",
    "ell",
    "eus",
    "fas",
    "fin",
    "fra",
    "glg",
    "heb",
    "hrv",
    "ind",
    "ita",
    "jpn",
    "nno",
    "nob",
    "pol",
    "por",
    "qcn",
    "slv",
    "spa",
    "swe",
    "tha",
    "zsm",
}
LANG_CODES = {
    "Arabic": "arb",
    "Bulgarian": "bul",
    "Catalan": "cat",
    "Danish": "dan",
    "Dutch": "nld",
    "German": "deu",
    "Greek": "ell",
    "English": "eng",
    "Basque": "eus",
    "Persian": "fas",
    "Finnish": "fin",
    "French": "fra",
    "Galician": "glg",
    "Hebrew": "heb",
    "Croatian": "hrv",
    "Indonesian": "ind",
    "Italian": "ita",
    "Japanese": "jpn",
    "Norwegian Nyorsk": "nno",
    "Norwegian Bokmal": "nob",
    "Polish": "pol",
    "Portuguese": "por",
    "Chinese": "qcn",
    "Slovenian": "slv",
    "Spanish": "spa",
    "Swedish": "swe",
    "Thai": "tha",
    "Malay": "zsm",
}
POS_ABBREVS_SORTED = [
    "n",
    "v",
    "a",
    "s",
    "r",
]  # sorted by likelihood of being Blissymbols
POS_FEATURE_DICT = {"n": 1, "v": 2, "a": 3, "s": 3, "r": 4}
POS_CODE_DICT = {
    1: "n",
    2: "v",
    3: "a",
    4: "r",
}  # always assign "a" to adjs, even satellites

# WIKTIONARY
# ----------
POS_WIKT_KEY = {  # Penn Treebank pos code mapped to Wiktionary pos
    "CC": "Conjunction",
    "IN": "Preposition",
    "CD": "Numeral",
    "LS": "Numeral",
    "DT": "Determiner",
    "PDT": "Determiner",
    "WDT": "Determiner",
    "PRP$": "Determiner",
    "WP$": "Determiner",
    "JJ": "Adjective",
    "JJR": "Adjective",
    "JJS": "Adjective",
    "NN": "Noun",
    "NNS": "Noun",
    "NNP": "Proper noun",
    "NNPS": "Proper noun",
    "RP": "Particle",
    "POS": "Particle",
    "TO": "Particle",
    "PRP": "Pronoun",
    "WP": "Pronoun",
    "RB": "Adverb",
    "RBR": "Adverb",
    "RBS": "Adverb",
    "WRB": "Adverb",
    "UH": "Interjection",
    "VB": "Verb",
    "VBD": "Verb",
    "VBG": "Verb",
    "VBN": "Verb",
    "VBP": "Verb",
    "VBZ": "Verb",
}
WIKTIONARY_POS_KEY = {
    "Conjunction": {"CC", "IN"},
    "Numeral": {"CD", "LS"},
    "Determiner": {"DT", "PDT", "WDT", "PRP$", "WP$"},
    "Article": {"DT"},
    "Preposition": {"IN"},
    "Adjective": {"JJ", "JJR", "JJS"},
    "Noun": {"NN"},  # can also be NNS
    "Proper noun": {"NNP"},  # can also be NNPS
    "Particle": {"RP", "POS", "TO"},
    "Pronoun": {"PRP", "WP"},
    "Adverb": {"RB", "RBR", "RBS", "WRB"},
    "Interjection": {"UH"},
    "Verb": {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"},
}
NOUNS = (
    WIKTIONARY_POS_KEY["Noun"].union(WIKTIONARY_POS_KEY["Proper noun"]).union({"NNS"})
)
PRONOUNS = WIKTIONARY_POS_KEY["Pronoun"].union({"NNPS"})
VERBS = WIKTIONARY_POS_KEY["Verb"]
ADJS = WIKTIONARY_POS_KEY["Adjective"]
ADVS = WIKTIONARY_POS_KEY["Adverb"]
OTHER = {
    "CC",
    "IN",
    "CD",
    "LS",
    "DT",
    "PDT",
    "WDT",
    "PRP$",
    "WP$",
    "POS",
    "TO",
    "PRP",
    "WP",
    "WRB",
    "UH",
}

# BLISSYMBOLS
# -----------
BLISS_SUPPORTED_LANGS = {
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
PUNCT_MAP = {
    ",": u"comma",
    ".": u"period,point,full_stop,decimal_point",
    "?": u"question_mark",
    "!": u"exclamation_mark",
}
POS_COLOURS = {
    "GRAY": {"INDICATOR"},
    "WHITE": set(PARTS_OF_SPEECH),  # WHITE is catch-all for other parts of speech
    "YELLOW": NOUNS,
    "RED": VERBS,
    "BLUE": NOUNS.union(PRONOUNS),
    "GREEN": ADJS.union(ADVS),
}
INDICATORS = {
    "thing": 1,
    "action": 1,
    "adverb": 1,
    "description": 1,
    "female": 2,
    "male": 2,
    "plural": 2,
    "neutral_form": 2,
    "object_form": 2,
    "diminutive_form": 2,
    "possessive": 2,
    "past_action": 3,
    "present_action": 3,
    "future_action": 3,
    "first_person": 4,
    "second_person": 4,
    "third_person": 4,
}
INDICATORS_MAP = {
    "plural": "plural",
    "possessive": "possessive_form",
    "first person": "first_person",
    "first-person": "first_person",
    "second person": "second_person",
    "second-person": "second_person",
    "third person": "third_person",
    "third-person": "third_person",
    "feminine": "female",
    "female": "female",
    "masculine": "action",
    "male": "action",
    "neuter": "neutral_form",
    "neutral": "neutral_form",
    "past": "past_action",
    "present": "present_action",
    "future": "future_action",
}
