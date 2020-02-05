# the line above tells Jupyter to write this cell to the file pig_latin.py

# remember pig latin?
def strip_punctuation(line):
    punctuation = ''
    line = line.strip()
    if len(line)>0:
        if line[-1] in ('.','!','?'):
            punctuation = line[-1]
            line = line[:-1]
    return line, punctuation

def pig_latin_sentence(sentence):
    # convert `sentence` into Pig Latin
    sentence, punctuation = strip_punctuation(sentence)
    sentence = sentence.split()
    new_words = []
    for word in sentence:
        endString= str(word[1:])
        them=endString, str(word[0:1]), 'ay'
        new_word="".join(them)
        new_words.append(new_word)
    new_sentence = ' '.join(new_words)
    new_sentence = new_sentence.lower()
    if len(new_sentence):
        new_sentence = new_sentence[0].upper() + new_sentence[1:]
    return new_sentence