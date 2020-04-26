import os 
from faker import Faker
from entry_creation_schemes import create_connection, create_news

faker = Faker()

from numpy import genfromtxt
import pandas as pd


def get_titles():
    path = os.path.join(os.getcwd(), "titles.xlsx")
    df = pd.read_excel(path)
    all = list(df['publish_date,headline_text'])
    headlines = [line.split(',')[1] for line in all]
    return headlines


def main_create_news():
    database_path = os.path.join(os.getcwd(), "data.db")

    # create a code connection
    conn = create_connection(database_path)
    titles = get_titles()
    with conn:
        # create a new project
        for i in range(100):
            title = titles[i]
            url = faker.domain_name()
            rating = 0.0
            review_count = 0
            category = 'unknown'
            user = (title, url, rating, review_count, category);
            user_id = create_news(conn, user)


if __name__ == '__main__':
    main_create_news()
