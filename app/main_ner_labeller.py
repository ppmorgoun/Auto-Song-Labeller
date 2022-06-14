from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
import spacy
import os
from pathlib import Path
import plac
from tkinter import Tk
from tkinter.filedialog import askdirectory
import sys
sys.path.append('/Users/petr/Documents/fun_stuff/auto_song_labeller/modules/')
import progress_bar as pg
import time

Tk().withdraw()
input_directory = askdirectory()

@plac.annotations(
    model_path=("Path to the pretrained spacy NER model. Defaults to ../output/model-last", "option", 'm', Path))

def main(input_directory=input_directory, model_path='../model/output/model-last'):
    """
    The main function that inputs a directory of songs (can have multiple subdirectories), walks through each individual file,
    passes the file name (less the .mp3 suffix) through the spacy NER model, then labels the file ID3 tags with the appropriate song and artist name

    """
    nlp = spacy.load(model_path) #load the model
    musicDirectory = input_directory
    for root,dirnames,fnames in os.walk(musicDirectory):
        l = len(fnames)
        pg_counter = 0
        pg.printProgressBar(pg_counter, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
        for fname in fnames:
    
            path = os.path.join(root, fname)
            
            text_data = fname[:-4]
            # Get the song and artist labels using our pretrained NER model
            doc = nlp(text_data)
            labels = {}
            for ent in doc.ents:
                labels[ent.label_] = ent.text
                
            # Read the ID3 tag or create one if not present
            try: 
                tags = ID3(path)
            except ID3NoHeaderError:
                print("Adding ID3 header")
                tags = ID3()
            try:
                tags["TIT2"] = TIT2(encoding=3, text=labels['SONG'])
            except:
                pass
            try:
                tags["TPE1"] = TPE1(encoding=3, text=labels['ARTIST'])
            except:
                pass
            
            path = os.path.join(root, fname)
            
            tags.save(path)

            #Update the progress bar
            time.sleep(0.1)
            pg_counter += 1
            pg.printProgressBar(pg_counter, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

if __name__ == '__main__':
    plac.call(main)