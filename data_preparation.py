import string
import re

def load_doc(filename):
    """
    Reads the passed file and returns its text.
    
    Parameters
        filename: str
            The name of the file to be read
    
    Returns
        : str
            The text read from the file.
    """
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

def clean_doc(doc):
    """
    Performs operations such as replacing punctuation, splitting, removing, and normalizing
    words to clean the passed text.

    Parameters
        doc: str 
            The piece of text to be processed.

    Returns
        : list
            The list of all words in the text (with duplicates).
    """
    doc = doc.replace('--', ' ') # replaces '--' with a space ' '
    tokens = doc.split() # splits into tokens by white space
    table = str.maketrans('', '', string.punctuation) # removes punctuation from each token
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()] # removes remaining tokens that are not alphabetic
    tokens = [word.lower() for word in tokens] # makes lower case
    return tokens

def organize_into_sequences(tokens, sequence_length):
    """
    Converts the passed tokens into word sequences (sentences)
    of the passed length.

    Parameters
        tokens: list
            A list of words.
        sequence_length: int
            The length of each resulting sentence in words.

    Returns
        : list
            The list of all sentences.
    """
    sequences = list()
    for i in range(sequence_length, len(tokens)):
        seq = tokens[i - sequence_length : i]
        line = ' '.join(seq)
        sequences.append(line)
    return sequences

def save_doc(sequences, filename):
    """
    Writes the passed sequences into a file. Each sequence
    corresponds to one line.

    Parameters
        sequences: list
            The list with all the sequences.
        filename: str
            The name of the file to write the sequences to.
    """
    file = open(filename, 'w')
    file.write('\n'.join(sequences))
    file.close()
    print(f'Sequences saved to file: {filename}')

"""
# load document
in_filename = 'republic_clean.txt'
doc = load_doc(in_filename)
print(doc[:200])

# clean document
tokens = clean_doc(doc)
print(tokens[:200])
print('Total Tokens: %d' % len(tokens))
print('Unique Tokens: %d' % len(set(tokens)))

# organize into sequences
sequences = organize_into_sequences(tokens, 51)
print('Total Sequences: %d' % len(sequences))

# save sequences to file
out_filename = 'republic_sequences.txt'
save_doc(sequences, out_filename)
"""
