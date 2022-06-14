# script to cache the dataset into a csv file
import sys
sys.path.append('/Users/petr/Documents/fun_stuff/auto_song_labeller/modules/')
import hdf5_getters as getters
import numpy as np
import pandas as pd
import os
import fnmatch

df = pd.DataFrame(columns=['Song Name', 'Artist'])

matches = list()
df_final = pd.DataFrame()
f= open("../data/MSD.csv","w")
for root,dirnames,filenames in os.walk('/Users/petr/Documents/fun_stuff/auto_song_labeller/data/MillionSongSubset'):
    for filename in fnmatch.filter(filenames, '*.h5'):
        #print(os.path.join(root, filename))
        hdf = pd.HDFStore(os.path.join(root, filename),mode ='r')
        artist = getters.get_artist_name(hdf).decode('UTF-8')
        #print(artist)
        name = getters.get_title(hdf).decode('UTF-8')
        #print(name)
        df1 = pd.DataFrame({'Song Name': [name], 'Artist': [artist]})
        df = pd.concat([df, df1], ignore_index=True, axis=0)
        hdf.close()
f.close()

df.to_csv("../data/MSD.csv")
