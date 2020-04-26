import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a code connection to the SQLite code
        specified by db_file
    :param db_file: code file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main_create_tables():

    database_path = os.path.join(os.getcwd(), "data.db")

    sql_create_users_table = '''CREATE TABLE IF NOT EXISTS users(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    first_name text NOT NULL, 
                                    last_name text NOT NULL, 
                                    email text NOT NULL,
                                    rating NUMERIC(9, 2),
                                    review_count integer );'''

    sql_create_news_table = '''CREATE TABLE IF NOT EXISTS news(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    title text NOT NULL,
                                    url text NOT NULL,
                                    rating NUMERIC(9, 2),
                                    review_count integer,
                                    category text ); '''

    sql_create_experts_table = ''' CREATE TABLE IF NOT EXISTS experts(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    email text NOT NULL );'''

    sql_create_user_transaction_table = '''CREATE TABLE IF NOT EXISTS transaction_users(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user_id integer NOT NULL,  
                                    news_id integer NOT NULL,  
                                    given_score integer NOT NULL, 
                                    FOREIGN KEY (user_id) REFERENCES users (id),
                                    FOREIGN KEY (news_id) REFERENCES news (id));'''

    sql_create_experts_transaction_table = '''CREATE TABLE IF NOT EXISTS transaction_experts(
                                    id integer PRIMARY KEY AUTOINCREMENT,  
                                    expert_id integer NOT NULL,   
                                    news_id integer NOT NULL,   
                                    given_score integer NOT NULL, 
                                    FOREIGN KEY (expert_id) REFERENCES experts(id),
                                    FOREIGN KEY (news_id) REFERENCES news(id) );'''
    # create a code connection
    conn = create_connection(database_path)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_news_table)
        create_table(conn, sql_create_experts_table)
        create_table(conn, sql_create_user_transaction_table)
        create_table(conn, sql_create_experts_transaction_table)

    else:
        print("Error! cannot create the code connection.")


if __name__ == '__main__':
    main_create_tables()
