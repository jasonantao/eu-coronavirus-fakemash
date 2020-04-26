import os 
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a code connection to a SQLite code """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    database_path = os.path.join(os.getcwd(), "data.db")
    create_connection(database_path)
