"""Adapted from https://github.com/MTG/andalusian-corpus-notebooks/blob/master/utilities/constants.py"""

import os


THIS_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(THIS_DIR, "../data")
RECORDINGS_DIR = os.path.join(DATA_DIR, "documents")
PLOT_DIR = os.path.join(THIS_DIR, "../plots")

# prefix applied to json file with the information from Dunya or derived by them
PREFIX_JSON = "andalusian_"

DF_LISTS = ["recording", "tab", "nawba", "mizan", "form", "description"]
COLUMNS_NAMES = ["name", "transliterated_name", "display_order", "uuid", "id"]
COLUMNS_RECORDINGS = ["title", "transliterated_title", "archive_url", "musescore_url"]
COLUMNS_DESCRIPTION = [
    "mbid",
    "section",
    "tab",
    "nawba",
    "mizan",
    "form",
    "start_time",
    "end_time",
    "duration",
]
STATISTIC_TYPE = [
    "# recordings",
    "# sections",
    "overall sections time",
    "avg sections time",
]

# Characteristics name (musical entities)
CHARACTERISTICS_NAMES = ["ṭāb‘", "nawba", "mīzān", "form"]
