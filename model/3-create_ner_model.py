import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import random
import json

nlp = spacy.blank('en')  # load a new spacy model
dbTrain = DocBin()  # create a DocBin object
dbVal = DocBin()
dataTest = []
inputData_path = '/Users/petr/Documents/fun_stuff/auto_song_labeller/data/nerData_list.txt'

with open(inputData_path, 'r') as f:
    trainData = json.loads(f.read())

for text, annot in trainData:  # data in previous format
    doc = nlp.make_doc(text)  # create doc object from text
    ents = []
    for start, end, label in annot['entities']:  # add character indexes
        print(start, end, label)
        span = doc.char_span(start, end, label=label,
                             alignment_mode='contract')
        if span is None:
            print('Skipping entity')
        else:
            ents.append(span)
    if random.random() <= 0.05:
        dataTest.append(text)
    elif random.random() <= 0.20:
        try:
            doc.ents = ents  # label the text with the ents
            dbVal.add(doc)
        except BaseException:
            print(text, annot)
    else:
        try:
            doc.ents = ents  # label the text with the ents
            dbTrain.add(doc)
        except BaseException:
            print(text, annot)

dbTrain_path = "/Users/petr/Documents/fun_stuff/auto_song_labeller/data/train.spacy"
dbVal_path = "/Users/petr/Documents/fun_stuff/auto_song_labeller/data/val.spacy"
testData_path = "/Users/petr/Documents/fun_stuff/auto_song_labeller/data/nerTestData.txt"
output_path = "/Users/petr/Documents/fun_stuff/auto_song_labeller/model/output/"

dbTrain.to_disk(dbTrain_path)  # save the docbin object
dbVal.to_disk(dbVal_path)
with open(testData_path, 'w') as f:
    f.write(json.dumps(dataTest))

print(
    f'\nCreated training, validation, and testing data sets. Saved Test Data to {testData_path}\n')
print(f'Created spacy formatted training and validation data sets. Please run the following command to train the model: \n')
print(
    f'python -m spacy train config.cfg --output {output_path} --paths.train {dbTrain_path} --paths.dev {dbVal_path}')
