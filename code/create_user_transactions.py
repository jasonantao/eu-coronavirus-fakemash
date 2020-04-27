import os
import random
from entry_creation_schemes import create_connection
from algorightms import compute_news_user_score, compute_user_rating_iterative


def get_user_info(conn, id):
    """
    get user attributes
    """

    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE id=?''', (id,))
    result = cur.fetchall()
    return result


def update_user_info(conn, user):
    """
    update user attributes
    """
    sql = ''' UPDATE users
              SET review_count = ?, rating = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


def update_news_info_final(conn, news):
    """
    update news attributes
    """
    sql = ''' UPDATE news
              SET review_count = ?, rating = ?, category = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, news)
    conn.commit()


def update_news_info(conn, news):
    """
    update news attributes
    """
    sql = ''' UPDATE news
              SET review_count = ?, rating = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, news)
    conn.commit()


def get_news_columns(conn, news_id):
    """
    get news attributes
    """
    cur = conn.cursor()
    cur.execute('''SELECT * FROM news WHERE id=?''', (news_id,))
    result = cur.fetchall()
    return result


def partition_list(r, n):
    list_in = list(range(1, r))
    random.seed(4)
    random.shuffle(list_in)
    first = int(0.9 * r)
    if n > 2:
        first = int(0.7 * r)
        last = int(0.9 * r)
        return list_in[:first], list_in[first:last], list_in[last:] 
    return list_in[:first], list_in[first:]


def get_category(score): 
    """
    category mapping
    """
    if score < 3:
        res = 'fake news'
    elif 3 <= score < 5:
        res = 'misleading'
    elif 4 <= score < 6.7:
        res = 'satire'
    else:
        res = 'legitimate'
    return res


def main():
    """
    Artificially creating user, their responses and changing tables values 
    """
    database_path = os.path.join(os.getcwd(), "data.db")

    # create a code connection
    conn = create_connection(database_path)

    with conn:
        valid = False
        satire = False
        valid_articles, fake_artickles, satire_articles = partition_list(101, 3)
        good_users, bad_users = partition_list(1001, 2)

        for id_news in range(1, 101):
            news_id = id_news
            if news_id in valid_articles:
                valid = True
            elif news_id in satire_articles:
                satire = True
            random_users = set()
            user_cnt = random.randint(50, 100)
            while len(random_users) < user_cnt:
                random_users.add(random.randint(1, 1000))

            for random_usr, user in enumerate(random_users):
                news_column = get_news_columns(conn, news_id)
                id, title, url, rating, review_count, category = news_column[0]
                if valid:
                    if user in good_users:
                        given_score = random.uniform(8.0, 10.0)
                    else:
                        given_score = random.uniform(2.0, 7.0)
                elif satire:
                    if user in good_users:
                        given_score = random.uniform(5.0, 7.0)
                    else:
                        given_score = random.uniform(7.5, 8.0)
                else:
                    if user in good_users:
                        given_score = random.uniform(2.0, 7.0)
                    else:
                        given_score = random.uniform(5.0, 10.0)

                user_info = get_user_info(conn, user)
                user_id, first_name, last_name, email, user_rating, user_cnt = user_info[0]

                news_new_rating, old_rating, review_count = compute_news_user_score(rating, review_count, given_score,
                                                                                    user_rating)
                update_news_info(conn, (review_count, round(news_new_rating, 3), id_news))

                user_new_rating, user_cnt = compute_user_rating_iterative(given_score, user_rating, user_cnt, old_rating, review_count - 1)
                update_user_info(conn, (user_cnt, round(user_new_rating, 3), user_id))


if __name__ == '__main__':
    main()
