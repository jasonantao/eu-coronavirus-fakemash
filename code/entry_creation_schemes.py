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
    except Error as e:
        print(e)

    return conn


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO users(first_name, last_name, email, rating, review_count)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def create_news(conn, news):
    """
    Create a new project into the projects table
    :param conn:
    :param news:
    :return: news id
    """
    sql = ''' INSERT INTO news(title, url, rating, review_count, category)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, news)
    return cur.lastrowid


def create_expert(conn, expert):
    """
    Create a new project into the projects table
    :param conn:
    :param expert:
    :return: user id
    """
    sql = ''' INSERT INTO experts(first_name, last_name, email)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, expert)
    return cur.lastrowid


def create_user_transaction(conn, user_transaction):
    """
    Create a new project into the projects table
    :param conn:
    :param user_transaction:
    :return: user id
    """
    sql = ''' INSERT INTO transaction_users(user_id, news_id, given_score)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user_transaction)
    return cur.lastrowid


def create_expert_transaction(conn, expert_transaction):
    """
    Create a new project into the projects table
    :param conn:
    :param expert_transaction:
    :return: expert id
    """
    sql = ''' INSERT INTO transaction_experts(expert_id, news_id, given_score)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, expert_transaction)
    return cur.lastrowid