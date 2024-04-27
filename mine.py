'''
text-miner
v.0.0.1 | Matt Briggs

'''

import yaml
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

    cd = CD.CorpusModel()
    cd.create(reportdb)

    conn = sqlite3.connect(corpusdb)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM document')
    corpus = cursor.fetchall()
    cursor.close()
    conn.close()

    # corpus loop
    records = len(corpus)
    counter = 0
    for i in corpus:
        doc_id, cor, path, ext, body, size = i
        counter += 1
        print('Processing {0} of {1}'.format(counter, records))

        # default analysis
        summary = SM.summarize_text(body)
        terms = TM.get_top_fifty(body, False)

        conn = sqlite3.connect(reportdb)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO documents (doc_id, doc_path, summary, ext, doc_length) VALUES (?, ?, ?, ?, ?)', (doc_id, path, summary, ext, size))
        conn.commit() 
        cursor.close()
        conn.close()

        # harvest all terms
        for key, value in terms.items():
            conn = sqlite3.connect(reportdb)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO raw_terms (doc_id, term, count) VALUES (?, ?, ?)', (doc_id, value['Keyword'], value['Count']))
            conn.commit() 
            cursor.close()
            conn.close()

    # get all unique terms and get line occurance
    conn = sqlite3.connect(reportdb)
    cursor = conn.cursor()
    cursor.execute('Select term from unique_terms')
    terms = cursor.fetchall()
    cursor.close()
    conn.close()

    for term_row in terms:
        term = term_row[0]
        squery = "SELECT * FROM lines WHERE line_text LIKE '%{}%'".format(term)
        try:
            conn = sqlite3.connect(corpusdb)
            cursor = conn.cursor()
            cursor.execute(squery)
            occurances = cursor.fetchall()
            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            print(e)

        term_occurances = []
        for occurance in occurances:
            new_row = (term,) + occurance
            term_occurances.append(new_row)

        conn = sqlite3.connect(reportdb)
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO kwic VALUES (?, ?, ?, ?, ?, ?, ?, ?)", term_occurances)
            conn.commit()  # Commit the changes
            print("Content for {} inserted successfully.".format(term))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()
 
if __name__ == "__main__":
    main()