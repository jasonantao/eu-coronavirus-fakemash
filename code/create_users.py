import os 
from faker import Faker
from entry_creation_schemes import create_connection, create_user

faker = Faker()


def main_create_users():
    database_path = os.path.join(os.getcwd(), "data.db")
    # create a code connection
    conn = create_connection(database_path)
    with conn:
        # create a new project
        for i in range(1000):
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = first_name + '_' + last_name + "@gmail.com"
            rating = 0.0
            review_count = 0
            user = (first_name, last_name, email, rating, review_count);
            user_id = create_user(conn, user)


if __name__ == '__main__':
    main_create_users()
