from data_preparation import load_doc
import nltk
import string

raw_text = load_doc('republic_clean.txt')
sentences = raw_text.split(". ")
#sentences = ["George said hello, and John is the brother of Mary.", "Is it true that DeepMind is a company at London?", "In Foo, a book written by Joe, physics is the main subject."]
subtree_relations = list()

for sentence in sentences:
    # remove all punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    #print(tagged_sentence)
    # <NNP> <.*>* (<VB.*> | <NN.*>) <IN> <NNP> # this will yield 'George brother of Mary', which is wrong

    # WHY DOES IT NOT PRINT THE LAST SENTENCE; (<VB.*> | <NN*>) does not print VBZ; WHY?
    chunk_rule = "RELATION: {<NNP> [^NNP]* (<VB.*> | <NN*>) <IN> <NNP>}" # properNoun, zero or more words (but not a properNoun), verb or noun, preposition, properNoun
    chunk_parser = nltk.RegexpParser(chunk_rule)
    tree = chunk_parser.parse(tagged_sentence)

    for subtree in tree.subtrees():
        if subtree.label() == 'RELATION':
            subtree_relations.append(subtree)
            #print(f'subtree = {subtree}')

# subtree to string
string_relations = set()
for relation in subtree_relations:
    relation = str(relation)[10:-1] # the first ten characters denote the subtree label; last character is parenthesis
    output = list()
    for word in relation.split():
        output.append(word.split('/')[0])    
    string_relations.add(' '.join(output[:1] + output[-3:])) # first word plus last three words
#print(string_relations)

def get_relations_to(entity):
    """
    Returns any relations that may exist relevant to the given word.

    Parameters
        entity: str
            A word given by the user. Must be a proper noun.
    
    Returns
        relations: list
            A list of strings each of which is composed of three words and represents a relation.
    """

    relations = list()
    for i in string_relations:
        if i.startswith(entity):
            relations.append(' '.join(i.split()[-3:])) # the first word of the relation is typed by the user; show the last three words
    return relations

def get_proper_nouns():
    """
    Returns all proper nouns.

    Returns
        proper_nouns: list
            All proper nouns that appear as the first word in the list of
            relations (each relation has the form: proper noun, preposition, proper noun).
    """

    proper_nouns = list()
    for relation in string_relations:
        first_proper_noun = relation.split(" ")[0]

        # discard some garbage; some three-letter words appear that are not proper nouns
        if len(first_proper_noun) > 3: proper_nouns.append(first_proper_noun)
    return proper_nouns
