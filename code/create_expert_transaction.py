import os 
from faker import Faker
from entry_creation_schemes import create_connection, create_expert_transaction

import random


def main_create_expert_transactions():
    database_path = os.path.join(os.getcwd(), "data.db")

    # create a code connection
    conn = create_connection(database_path)
    with conn:
        # create a new project
        for i in range(200):
            expert_id = random.randint(1, 100)
            news_id = random.randint(1, 100)
            given_score = round(random.uniform(1.0, 10.0), 2)
            tr_expert = (expert_id, news_id, given_score)
            tr_expert_id = create_expert_transaction(conn, tr_expert)


if __name__ == '__main__':
    main_create_expert_transactions()
