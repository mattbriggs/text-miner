'''
text-miner
v.0.0.1 | Matt Briggs

'''

import yaml
import sqlite3

import createdatabase as CD
import terms as TM
import summary as SM


def call_sql(sql, db):
    if not isinstance(sql, str) or not sql.strip():
        return "Invalid SQL query: Query is empty or not a string."

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Check if the query is a SELECT statement (to decide on fetching data)
        if sql.strip().lower().startswith('select'):
            cursor.execute(sql)
            data = cursor.fetchall()  # Fetch data for SELECT statements
        else:
            cursor.execute(sql)
            conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
            data = "Query executed successfully."

    except sqlite3.Error as e:
        data = f"SQL Error: {e}"
    finally:
        cursor.close()
        conn.close()

    return data


def main():
    '''Run the main program.'''
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    corpusdb = cfg['corpusdb']
    reportdb = cfg['reportdb']

    cd = CD.CorpusModel()
    cd.create(reportdb)

    corpus = call_sql('SELECT * FROM document', corpusdb)

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

        squery = 'INSERT INTO documents (doc_id, doc_path, summary, ext, doc_length) VALUES (?, ?, ?, ?, ?) ', (doc_id, path, summary, ext, size)
        data = call_sql(squery, reportdb)
        print(data)

        # harvest all terms
        for key, value in terms.items():
            squery = 'INSERT INTO raw_terms (doc_id, term, count) VALUES (?, ?, ?) ', (doc_id, value['Keyword'], value['Count'])
            data = call_sql(squery, reportdb)
            print(data)

        # get all unique terms and get line occurance
        squery = 'Select term from unique_terms'
        terms = call_sql(squery, reportdb)

        for term in terms:
            squery = "Select * from lines Where line_text LIKE '%{}%';".format(term)
            occurances = call_sql(squery, reportdb)
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