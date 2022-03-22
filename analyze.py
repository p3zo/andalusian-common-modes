"""Adapted from https://github.com/MTG/andalusian-corpus-notebooks/blob/master/utilities/metadataStatistics.py"""

import collections
import itertools
import json
import os
import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from music21 import converter, interval

from utils.constants import (
    COLUMNS_DESCRIPTION,
    COLUMNS_NAMES,
    COLUMNS_RECORDINGS,
    DATA_DIR,
    DF_LISTS,
    PLOT_DIR,
    RECORDINGS_DIR,
)
from utils.generalUtilities import get_interval, get_seconds

pd.set_option("display.max_rows", None)
sns.set_style()


def get_recordings_df():
    # Create a dataframe for every json file
    recording_data_filepath = "andalusian_recording.json"

    with open(os.path.join(DATA_DIR, recording_data_filepath)) as json_file:
        recordings_data = json.load(json_file)

    df = pd.DataFrame(columns=COLUMNS_RECORDINGS)

    # fill the first part of recordings dataframe with the data from recording dataframe
    for row in recordings_data["results"]:
        new_row = pd.DataFrame(
            {
                COLUMNS_RECORDINGS[0]: row[COLUMNS_RECORDINGS[0]],
                COLUMNS_RECORDINGS[1]: row[COLUMNS_RECORDINGS[1]],
                COLUMNS_RECORDINGS[2]: None,
                COLUMNS_RECORDINGS[3]: None,
            },
            index=[row[COLUMNS_DESCRIPTION[0]]],
        )
        df = pd.concat([df, new_row])

    return df


def get_description_data():
    filepath = "andalusian_description.json"
    with open(os.path.join(DATA_DIR, filepath)) as json_file:
        descriptions = json.load(json_file)
    return descriptions


def get_df_list():
    df_list = []
    id_name = "uuid"

    # NB: indexes of the following dataframes are the id of every object in the json file
    for i in range(1, 5):
        # create a dataframe for each list
        columns = [i for i in COLUMNS_NAMES[0:3] if i != "display_order"]
        df = pd.DataFrame(columns=columns)
        with open(
            os.path.join(DATA_DIR, f"andalusian_{DF_LISTS[i]}.json")
        ) as json_file:
            file = json.load(json_file)

        for row in file["results"]:
            if (id_name not in row) and id_name == id_name:
                id_name = "id"

            new_row = pd.DataFrame(
                {
                    COLUMNS_NAMES[0]: row[COLUMNS_NAMES[0]],
                    COLUMNS_NAMES[1]: row[COLUMNS_NAMES[1]],
                },
                index=[row[id_name]],
            )
            df = pd.concat([df, new_row])
        df_list.append(df)

    df_tab = df_list[0]
    df_nawba = df_list[1]
    df_mizan = df_list[2]
    df_form = df_list[3]

    return df_tab, df_nawba, df_mizan, df_form


def get_description_df(recordings_df):

    description_df = pd.DataFrame(columns=COLUMNS_DESCRIPTION)

    mbid_no_sections = []

    description_data = get_description_data()

    counter = 0
    for row in description_data:
        # fill the second part of the recording dataframe
        recordings_df.at[row[COLUMNS_DESCRIPTION[0]], COLUMNS_RECORDINGS[2]] = row[
            COLUMNS_RECORDINGS[2]
        ]
        recordings_df.at[row[COLUMNS_DESCRIPTION[0]], COLUMNS_RECORDINGS[3]] = row[
            COLUMNS_RECORDINGS[3]
        ]

        # fill the description dataframe
        mbid = row[COLUMNS_DESCRIPTION[0]]
        section_counter = 0
        if not row["sections"]:
            mbid_no_sections.append(mbid)

        for section in row["sections"]:
            tab = section[COLUMNS_DESCRIPTION[2]]["id"]
            nawba = section[COLUMNS_DESCRIPTION[3]]["id"]
            mizan = section[COLUMNS_DESCRIPTION[4]]["id"]
            form = section[COLUMNS_DESCRIPTION[5]]["id"]
            start_time = get_seconds(section[COLUMNS_DESCRIPTION[6]])
            end_time = get_seconds(section[COLUMNS_DESCRIPTION[7]])
            duration = get_interval(
                section[COLUMNS_DESCRIPTION[7]], section[COLUMNS_DESCRIPTION[6]]
            )

            description_df.loc[counter] = [
                mbid,
                section_counter,
                tab,
                nawba,
                mizan,
                form,
                start_time,
                end_time,
                duration,
            ]
            section_counter += 1
            counter += 1

    return description_df


def plot_intervals(pair_intervals, tab):
    """Create a figure with subplots for each interval distribution of a given tab"""
    fig = plt.figure(figsize=(12, 4))

    intervals_by_mizan = [
        (k.split("_")[1], v) for k, v in pair_intervals.items() if tab in k
    ]

    for ix, (mizan, mizan_intervals) in enumerate(intervals_by_mizan):
        print(f"Plotting {tab} with {mizan}")
        # To order the intervals, create a dict with the equivalence of
        # each interval's size in semitones and its name
        ordered_intervals = {}
        for k in mizan_intervals.keys():
            itv = interval.Interval(k)
            ordered_intervals[itv.semitones] = k

        # Ordered list of intervals by semitones size
        xValues = sorted(ordered_intervals.keys())

        # Ordered list of interval names by their semitiones size
        xTicks = [ordered_intervals[i] for i in xValues]

        # Ordered list of y axis values
        yValues = np.array([mizan_intervals[i] for i in xTicks])

        # Normalize yValues for better comparison
        n_intervals = sum(yValues)
        print(f"  Num intervals: {n_intervals}")
        yValues = yValues / n_intervals

        # Create the subplot
        plt.subplot(int(f"1{len(intervals_by_mizan)}{ix+1}"))
        plt.bar(xValues, yValues, zorder=3)
        plt.xticks(xValues, xTicks)
        plt.grid(zorder=0, axis="y", lw=0.25)

        # Common x and y axes limits
        plt.xlim(-1, 13)
        plt.ylim(0, 0.5)
        plt.title(mizan)
        plt.tight_layout()

    # Create a big subplot for shared labels
    ax = fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor="none", top="off", bottom="off", left="off", right="off")
    ax.set_title(tab, pad=25)
    ax.set_ylabel("percent of intervals", labelpad=8)
    plt.tight_layout()

    filepath = os.path.join(PLOT_DIR, f"{tab}.png")
    plt.savefig(filepath)
    print(f"  Saved {filepath}")

    plt.clf()


if __name__ == "__main__":
    description_data = get_description_data()

    # How does the distribution of intervals played in a melodic mode change
    # when different rhythmic modes are being played?
    tubu = ["al-istihlāl", "rumil al-māīyah"]
    mawazin = ["qdām", "basīṭ", "bṭāyḥī"]

    mode_pairs = itertools.product(tubu, mawazin)

    # Make the transliterated english names consistent with other sources
    name_mapping = {
        "basīṭ": "basít",
        "qdām": "quddám",
        "rumil al-māīyah": "raml al-maya",
        "al-istihlāl": "al-istihlāl",
        "bṭāyḥī": "btāyhī",
    }

    # Initialize a nested dict for {pair_name: {intervals}}
    intervals = collections.defaultdict(dict)

    # Also keep track of how many scores the combined pairs are used in
    n_scores = collections.defaultdict(int)

    for mode_pair in mode_pairs:
        print(mode_pair)

        tab, mizan = mode_pair
        tab_name = name_mapping[tab]
        mizan_name = name_mapping[mizan]
        pair_name = f"{tab_name}_{mizan_name}"

        # Get the times of sections of interest from the performance metadata
        mode_pair_sections = {}
        for score in description_data:
            score_mode_pair_sections = [
                i
                for i in score["sections"]
                if i["tab"]["transliterated_name"] == tab
                and i["mizan"]["transliterated_name"] == mizan
            ]
            if len(score_mode_pair_sections) > 0:
                mode_pair_sections[score["mbid"]] = score_mode_pair_sections

        # Parse the scores
        for mbid in mode_pair_sections.keys():
            print(f"  Loading {mbid}.xml...")

            s = converter.parse(os.path.join(RECORDINGS_DIR, mbid, mbid + ".xml"))

            # Rests are important when counting melodic intervals
            nr = s.flat.notesAndRests.stream()

            score = mode_pair_sections[mbid]
            n_scores[pair_name] += 1

            for section in score:
                tab = section["tab"]["transliterated_name"]

                start_secs = get_seconds(section["start_time"])
                end_secs = get_seconds(section["end_time"])

                # All the notes in the current section
                sectionNotes = nr.getElementsByOffset(start_secs, end_secs).stream()

                for n in sectionNotes[:-1]:
                    # All notes are included, even grace notes
                    if n.isNote and n.next().isNote:
                        itv = interval.Interval(n, n.next())
                        intervals[pair_name][itv.name] = (
                            intervals[pair_name].get(itv.name, 0) + 1
                        )

    for tab in tubu:
        plot_intervals(intervals, name_mapping[tab])

    print("Number of scores by mode pair:")
    pprint.pprint(n_scores)
