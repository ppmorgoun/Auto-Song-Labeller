import re

def clean_text(text):
    # Remove non-alphanumeric characters
    text = re.sub('[^a-zA-Z\- ]', '', text)

    # lowercase text 
    text = text.lower()
    
    return text