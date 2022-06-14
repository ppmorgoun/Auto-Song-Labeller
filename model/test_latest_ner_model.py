# loading and testing the model
import spacy
import json

nlp = spacy.load('/Users/petr/Documents/fun_stuff/auto_song_labeller/model/output/model-last') #load the model
with open('/Users/petr/Documents/fun_stuff/auto_song_labeller/data/nerTestData.txt', 'r') as f:
    dataTest = json.loads(f.read())
print(f"Number of test examples: {len(dataTest)}")

test_docs_converted = [nlp(doc) for doc in dataTest]

for i in range(len(test_docs_converted)):
    converted_doc = test_docs_converted[i]
    text = dataTest[i]
    for ent in converted_doc.ents:
        print(ent.label_, ent.text)
    print(f"Actual text: {text}".format(text=text))
    print('___________________')


