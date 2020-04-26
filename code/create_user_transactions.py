from entry_creation_schemes import create_connection

import random
import os


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


def compute_news_user_score(news_rating, review_count, given_score, user_rating):
    """
    iteratively re-calculate news attributes 
    """
    discount_factor = 1
    if review_count == 0:
        raw_news_rating = discount_factor * given_score
        new_rating = discount_factor * user_rating * raw_news_rating
        review_count = review_count + 1
    else:
        average = review_count * news_rating
        review_count = review_count + 1
        new_rating = (average + user_rating * given_score) / review_count
        discount_quanity = 1 - (1.0/review_count)
        p = 0.5
        # first_part = new_average * p
        # second_part = 10 * (1 - p) * (1 - math.exp(- review_count / 100))
    return new_rating, news_rating, review_count


def compute_user_rating_iterative(given_score, user_rating, user_cnt, old_score, news_count): 
    """
    iteratively re-calculate user attributes 
    """
    # discount user experience
    diff_new = abs(given_score - old_score)
    max_diff = 9

    if user_cnt == 0:
        raw_user_rating = (1 - diff_new / max_diff)
        discount_factor = 0.5
        user_new_rating = raw_user_rating * discount_factor
        user_cnt = user_cnt + 1
    else:
        discounting_user_factor = 1 - (1/user_cnt)
        raw_user_rating = 1 - (diff_new/27)
        user_new_rating = (user_rating * user_cnt + raw_user_rating) / (user_cnt + 1)
        user_new_rating = discounting_user_factor * user_new_rating
        user_cnt = user_cnt + 1

    return user_new_rating, user_cnt


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
