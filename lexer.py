import re

def tokenize(text):
    text = text.lower()
    return re.findall(r'[a-z]+|\d+', text)