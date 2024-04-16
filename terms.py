''' Extract terms from a document.

    This script will parse a markdown document. It will extract noun
    entities with more than one word from each markdown topic.

    1. Call `get_top_fifty(inpath, False)`
    2. Output will output a dict object with the following attributes:
    - Count. Number of words in the topic.
    - Keyword: the keyword entity. Default is to find 2 or more word phrases.
    - Page: filepath to the file.

    Note: stoplist.py contains a list of strings to remove from the parse.

    Matt Briggs V1.3: 5.25.2021
'''

import nltk
import pandas as pd
from prettytable import PrettyTable
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import stoplist as SP

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')

def print_dict_rank(indict):
    '''Prints a ranked list of keywords from the dictionary provided.'''
    x = PrettyTable()
    print("Keyword scores for + {}\n".format(indict[1]["page"]))
    x.field_names = ["Rank", "Keyword"]
    for i in indict.keys():
        x.add_row([indict[i]["score rank"], indict[i]["keyword"]])
    x.align["Keyword"] = "l"
    print(x)

def clean_keyword(inlist):
    '''Removes specified characters from text elements in the list.'''
    glyphs = '[]|<>*=@_+Â/~'
    outlist = []
    for i in inlist:
        for char in glyphs:
            i = i.replace(char, "")
        outlist.append(i)
    return outlist

def remove_blank(inlist):
    '''Removes blank entries from the list.'''
    noblank = []
    for i in inlist:
        x = i.strip()
        if x:
            noblank.append(x)
    return noblank

def apply_stoplist(inlist):
    '''Removes stop words from the list using the custom stoplist.'''
    stoplist = SP.stoplist.split("\n")
    filtered_words = [i for i in inlist if i not in stoplist]
    return filtered_words

def extract_chunks(sent):
    '''Extracts noun phrases from a sentence.'''
    grammar = r"""
    NBAR:
        {<NN.*>*<NN.*>}

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    lemmatizer = WordNetLemmatizer()
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        term = ' '.join([child[0] for child in tree.leaves()])
        lemmatized_term = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(term)])
        ne.add(lemmatized_term)
    return ne

def parse_sentences(incorpus):
    '''Splits text into a list of sentences.'''
    sentences = nltk.sent_tokenize(incorpus)
    return sentences

def only_word_pairs(inlist):
    '''Filters out single words, keeping only phrases.'''
    return [i for i in inlist if len(i.split()) > 1]

def extract_entities(bodytext, single=False):
    '''Extracts unique noun entities from text.'''
    entities = []
    for sent in parse_sentences(bodytext):
        entities.extend(extract_chunks(sent))
    entities = clean_keyword(entities)
    entities = remove_blank(entities)
    unique_entities = set(entities)
    if not single:
        unique_entities = only_word_pairs(list(unique_entities))
    return apply_stoplist(list(unique_entities))

def get_top_fifty(instring, single=False):
    '''Analyzes a markdown file and returns the top 50 keywords.'''
    try:
        record_terms = extract_entities(instring, single)
        pagedata = {"Count": [], "Keyword": []}
        for term in record_terms:
            pagedata["Count"].append(instring.count(term))
            pagedata["Keyword"].append(term)
        term_df_full = pd.DataFrame(pagedata).sort_values(by=["Count"], ascending=False).reset_index()
        term_summary = term_df_full.loc[:50].to_dict('records')
        term_out = {i + 1: term for i, term in enumerate(term_summary)}
    except Exception as e:
        term_out = {1: {"error": "Unable to process file.", "message": str(e)}}
    return term_out

def main():
    print("This is the script that contains the functional logic.")

if __name__ == "__main__":
    main()
