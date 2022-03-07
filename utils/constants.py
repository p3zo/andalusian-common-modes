"""Adapted from https://github.com/MTG/andalusian-corpus-notebooks/blob/master/utilities/constants.py"""

import os


# change parameters here to customize the directories where data will be stored.
# NB: the source directory is the main directory of the notebook
DATA_DIR = "data"
RECORDINGS_DIR = os.path.join(DATA_DIR, "documents")

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
