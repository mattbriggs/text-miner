'''
Create the relational datamodel of a corpus.
v.1.0.0 2022.2.10
'''

import os
import sqlite3

class CorpusModel():
    '''The corpus model creator creates a set of tables in a database for the ore model.'''

    def __init__(self):
        pass

    def create(self, inpath):
        '''With an incoming path, create an empty sqldatabase.'''

        try:
            sqliteConnection = sqlite3.connect(inpath)
            cursor = sqliteConnection.cursor()
            print("Successfully connected to SQLite")

            with open('ore.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
            cursor.executescript(sql_script)
            print("SQLite script executed successfully")
            cursor.close()

        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)