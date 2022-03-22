"""Adapted from https://github.com/MTG/andalusian-corpus-notebooks/blob/master/utilities/generalutilities.py"""

import time


def get_interval(end, start):
    e = time.strptime(end, "%H:%M:%S")
    e_sec = e.tm_sec + e.tm_min * 60 + e.tm_hour * 3600
    s = time.strptime(start, "%H:%M:%S")
    s_sec = s.tm_sec + s.tm_min * 60 + s.tm_hour * 3600
    return e_sec - s_sec


def get_seconds(value_in_sec):
    e = time.strptime(value_in_sec, "%H:%M:%S")
    return e.tm_sec + e.tm_min * 60 + e.tm_hour * 3600


def get_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0}:{1:02d}:{2:02d}".format(h, m, s)


def list_intersection(a, b):
    c = list()
    for e in a:
        if e in b:
            c.append(e)
    return c
