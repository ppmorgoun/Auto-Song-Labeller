from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
import spacy
import os

nlp = spacy.load('/Users/petr/Documents/fun_stuff/youtube_app/output/model-last/') #load the model
musicDirectory = '/Users/petr/Documents/fun_stuff/youtube_app/Music'
for root,dirnames,fnames in os.walk(musicDirectory):
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