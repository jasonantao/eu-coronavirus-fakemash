import math 


def compute_news_user_score(news_rating, review_count, given_score, user_rating):
    """
    iteratively re-calculate news attributes 
    """
    discount_factor = 0.1
    if review_count == 0:
        raw_news_rating = discount_factor * given_score
        new_rating = discount_factor * user_rating * raw_news_rating
        review_count = review_count + 1
    else:
        average = review_count * news_rating
        review_count = review_count + 1
        weighted_average = (average + user_rating * given_score) / review_count 
        p = 0.5
        weighted_average = weighted_average * p
        discounting_count_factor = 10 * (1 - p) * (1 - math.exp(- review_count / 100))
        new_rating = weighted_average + discounting_count_factor
    return new_rating, news_rating, review_count


def compute_user_rating_iterative(given_score, user_rating, user_cnt, old_score, news_count): 
    """
    iteratively re-calculate user attributes 
    """
    diff_new = abs(given_score - old_score)
    max_diff = 9

    if user_cnt == 0:
        raw_user_rating = (1 - diff_new / max_diff)
        discounting_user_factor = 0.3
        user_new_rating = raw_user_rating * discounting_user_factor
        user_cnt = user_cnt + 1
    else:
        discounting_user_factor = 1 - (1/user_cnt)
        raw_user_rating = 1 - (diff_new/27)
        user_new_rating = (user_rating * user_cnt + raw_user_rating) / (user_cnt + 1)
        user_new_rating = discounting_user_factor * user_new_rating
        user_cnt = user_cnt + 1

    return user_new_rating, user_cnt
