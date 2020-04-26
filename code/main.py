from tables import main_create_tables
from create_experts import main_create_experts
from create_news import main_create_news
from create_users import main_create_users
from create_expert_transaction import main_create_expert_transactions
from compute_user_ratings import main_create_compute_user_rating

if __name__ == '__main__':
    main_create_tables()
    main_create_experts()
    main_create_news()
    main_create_users()
    main_create_expert_transactions()
    main_create_compute_user_rating()
