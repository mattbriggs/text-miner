import sqlite3

def search_terms(db_path, search_term):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Perform a full-text search query
    cursor.execute("SELECT line_number, line_text FROM text_lines_fts WHERE line_text MATCH ?", (search_term,))
    results = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    return results

# Usage
db_path = 'C:\\data\\20240405test\\corpus.db'
search_term = 'Azure Stack Hub'
results = search_terms(db_path, search_term)
for result in results:
    print(result)
