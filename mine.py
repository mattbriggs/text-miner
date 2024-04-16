'''
text-miner
v.0.0.1 | Matt Briggs

'''

import yaml
import os
import sqlite3

import createdatabase as CD
import terms as TM
import summary as SM

def main():
    '''Run the main program.'''
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    corpusdb = cfg['corpusdb']
    reportdb = cfg['reportdb']

    # get the corpus
    conn = sqlite3.connect(corpusdb)
    cursor = conn.cursor()
    query_sql = 'SELECT * FROM document'
    cursor.execute(query_sql)
    corpus = cursor.fetchall()

    cd = CD.CorpusModel()
    cd.create(reportdb)

    for i in corpus:
        doc_id, corpus, path, ext, body, size = i

        # load document
        print(path)
        # get summary
        summary = SM.summarize_text(body)
        print(len(summary))

        # get termsclear
        terms = TM.get_top_fifty(body, False)
        print(terms)



if __name__ == "__main__":
    main()
