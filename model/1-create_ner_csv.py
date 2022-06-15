# script to extract the raw .h5 music files data into a csv file
import fnmatch
import os
import pandas as pd
import numpy as np
import hdf5_getters as getters
import sys
sys.path.append('/Users/petr/Documents/fun_stuff/auto_song_labeller/modules/')

df = pd.DataFrame(columns=['Song Name', 'Artist'])

matches = list()
df_final = pd.DataFrame()

f = open("../data/MSD.csv", "w")
for root, dirnames, filenames in os.walk(
        '/Users/petr/Documents/fun_stuff/auto_song_labeller/data/MillionSongSubset'):
    for filename in fnmatch.filter(filenames, '*.h5'):
        # Looks through the directory for each file that has a .h5 file extension, and pulls
        # the fields I care about
        hdf = pd.HDFStore(os.path.join(root, filename), mode='r')
        artist = getters.get_artist_name(hdf).decode('UTF-8')
        # print(artist)
        name = getters.get_title(hdf).decode('UTF-8')
        # print(name)
        df1 = pd.DataFrame({'Song Name': [name], 'Artist': [artist]})
        df = pd.concat([df, df1], ignore_index=True, axis=0)
        hdf.close()
f.close()

df.to_csv("../data/MSD.csv")
