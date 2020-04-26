from faker import Faker
import os 
from entry_creation_schemes import create_connection, create_expert

faker = Faker()


def main_create_experts():
    database_path = os.path.join(os.getcwd(), "data.db")

    # create a code connection
    conn = create_connection(database_path)
    with conn:
        # create a new project
        for i in range(100):
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = first_name + '_' + last_name + "@gmail.com"
            expert = (first_name, last_name, email);
            expert_id = create_expert(conn, expert)


if __name__ == '__main__':
    main_create_experts()
