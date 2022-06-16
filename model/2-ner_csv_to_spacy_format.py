# preprocessing data into correct form for spacy
# following tutorial
import spacy
from spacy.tokens import DocBin
import random
import json
import re
import pickle
import pandas as pd
import sys
sys.path.append('/Users/petr/Documents/fun_stuff/auto_song_labeller/modules/')
import clean_text as ct

df = pd.read_csv("../data/MSD.csv", index_col=0)
trainData = []
raw_text = []
output_path = '/Users/petr/Documents/fun_stuff/auto_song_labeller/data/nerData_list.txt'

entities = {"SONG": "ARTIST"}

for idx, row in df.iterrows():
    # turn song name into a string in case it isn't, and strip
    # leading/trailing whitespace
    song = str(row[0]).strip()
    #song = ct.clean_text(song) # remove non alphanumeric characters excluding the dash "-" and make lowercase
    artist = str(row[1]).strip()  # same for artist name
    #artist = ct.clean_text(artist) # remove non alphanumeric characters excluding the dash "-" and make lowercase

    try:  # fetching the length of the song name if it exists
        len_song = len(song)
    except BaseException:
        len_song = 0
    try:  # fetching the length of the artist name if it exists
        len_artist = len(artist)
    except BaseException:
        len_artist = 0

    #text = song + ' - ' + artist
    songFirst = True
    if len_song != 0 and len_artist != 0:
        if random.random() <= 0.5:  # making it so the artist is first 50% of the time
            cleanText = song + ' - ' + artist
        else:
            cleanText = artist + ' - ' + song
            songFirst = False
    else:
        cleanText = song

    if random.random() <= 0.05:  # adding some non-entity strings to roughly match the frequency in youtube videos
        cleanText += ' (OFFICIAL MUSIC VIDEO)'
    dict_value = []

    raw_text.append(cleanText)
    # In the case where neither song nor artist is None:
    if song is not None and artist is not None:
        ents = []
        for songEnt, artistEnt in entities.items():
            if songFirst:
                ent_song = (0, len_song, songEnt)
                ents.append(ent_song)

                ent_artist = (
                    len_song + 3,
                    len_song + 3 + len_artist,
                    artistEnt)  # with dash
                ents.append(ent_artist)
            else:
                ent_song = (len_artist + 3, len_artist + 3 + len_song, songEnt)
                ents.append(ent_song)

                ent_artist = (0, len_artist, artistEnt)  # with dash
                ents.append(ent_artist)

    # for the case where there is only a song name:
    elif song is not None:
        ents = []
        for songEnt, _ in entities.items():
            ent_song = (0, len_song, songEnt)
            print('4')
            print(ent_song)
            ents.append(ent_song)
    # for the case there is only an artist somehow:
    else:
        ents = []
        for _, artistEnt in entities.items():
            ent_artist = (0, len_artist, artistEnt)  # with dash

            ents.append(ent_artist)

    print(ents)
    entsDict = {}
    entsDict["entities"] = ents
    trainingExample = (cleanText, entsDict)
    trainData.append(trainingExample)

with open(output_path, 'w') as f:
    f.write(json.dumps(trainData))
print(
    f"Created text file with 10,000 songs and artists, saved to {output_path}")
