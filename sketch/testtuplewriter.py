import sqlite3

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