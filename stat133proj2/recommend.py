import random
import json
from math import sqrt
import numpy as np

with open('./processed_data/onlyfood_users.txt','r') as inf:
    dict_from_file = json.load(inf)
    data = dict_from_file

def get_business_ids(user_id):
    """returns a dictionary of {business_id: {"rating": NA, "state": NA, "city": NA}} """
    return data[user_id]["reviews"]

def get_rating(user_id,business_id):
    return data[user_id]["reviews"][business_id]["rating"]

def get_category(user_id,business_id):
    return data[user_id]["reviews"][business_id]["categories"]

def distance_method(user_id1, user_id2, r):
    distance = 0
    common_rating = False
    user1_business_ids = get_business_ids(user_id1)
    user2_business_ids = get_business_ids(user_id2)
    if len(set(user2_business_ids).difference(set(user1_business_ids))) == 0:
        return 10000

    for business_id in list(user1_business_ids.keys()):
        if business_id in list(user2_business_ids.keys()):
            distance += pow(abs(get_rating(user_id1,business_id)-get_rating(user_id2,business_id)), r)
            common_rating = True

    if common_rating:
        return pow(distance, 1/r)
    else:
        return None

def nearest_with_user(user_id1,r):
    """returns a user with the nearest distance as user_id1
    manhattan: r = 1
    euclidean: r = 2
    """
    names_by_distance = []
    otherusers_lst = list(data.keys())
    otherusers_lst.remove(user_id1)

    for otheruser in otherusers_lst:
        distance = distance_method(user_id1,otheruser,r)
        if distance:
            names_by_distance.append((distance,otheruser))
    names_by_distance.sort()
    return names_by_distance[0][1]

def recommend_new_restaurant(user_id1,method='manhattan'):
    """give a list of recommended businesses and their ratings
    using method: manhattan or euclidean"""
    recommendations = []

    if method == 'manhattan':
        neighbor = nearest_with_user(user_id1,1)

    elif method == 'euclidean':
        neighbor = nearest_with_user(user_id1,2)

    elif method == 'cosine':
        neighbor = highest_cosine_user(user_id1)

    elif method == 'pearson':
        neighbor = highest_correlation(user_id1)
    
    neighbor_reviews = get_business_ids(neighbor)
    user_reviews = get_business_ids(user_id1)    

    for business_id in neighbor_reviews:
        if business_id not in user_reviews:
            recommendations.append((business_id,get_rating(neighbor,business_id)))
    return recommendations

def highest_correlation(user_id1):
    """returns a user with the highest correlation with user_id1"""
    correlation_lst = []
    otherusers_lst = list(data.keys())
    otherusers_lst.remove(user_id1)

    for otheruser in otherusers_lst:
        correlation_lst.append((correlation(user_id1,otheruser),otheruser))
    print('highest correlation is', max(correlation_lst)[0]) #for testing
    return max(correlation_lst)[1]

def correlation(user_id1,user_id2):
    n = 0; xy = 0; x = 0; y = 0; sq_y = 0; sq_x = 0
    user1_business_ids = get_business_ids(user_id1)
    user2_business_ids = get_business_ids(user_id2)

    for business_id in list(user1_business_ids.keys()):
        if business_id in list(user2_business_ids.keys()):
            n += 1
            rating_by_user_1 = get_rating(user_id1,business_id)
            rating_by_user_2 = get_rating(user_id2,business_id)
            x = x + rating_by_user_1
            y = y + rating_by_user_2
            xy = xy + rating_by_user_1*rating_by_user_2
            sq_y = sq_y + rating_by_user_1**2
            sq_x = sq_x + rating_by_user_2**2

    if n == 0:
        return 0

    else:
        denominator = sqrt(abs(sq_x - float(x**2) / n)) * sqrt(abs(sq_y - float(y**2) / n))
        if denominator == 0:
            return 0
        else:
            corr = (xy -( x * y) / n) / denominator
            return corr


def cosine_similarity(user_1, user_2):
    business1 = dict_from_file[user_1]["reviews"].keys()
    business2 = dict_from_file[user_2]["reviews"].keys()
    if len(set(business2).difference(set(business1))) == 0:
        return 0.0
    business1.extend(business2)
    businesses = set(business1)
    ratings_1 = []
    ratings_2 = []
    for business in businesses:
        if dict_from_file[user_1]["reviews"].has_key(business):
            ratings_1.append(dict_from_file[user_1]["reviews"][business]["rating"])
        else:
            ratings_1.append(0)
        if dict_from_file[user_2]["reviews"].has_key(business):
            ratings_2.append(dict_from_file[user_2]["reviews"][business]["rating"])
        else:
            ratings_2.append(0)
    
    return float(np.dot(ratings_1, ratings_2) / sqrt(np.dot(ratings_1, ratings_1) * np.dot(ratings_2, ratings_2)))


def highest_cosine_user(user1):
    maximum_correlation = -1000.0
    maximum_user = None

    otherusers_lst = list(data.keys())
    otherusers_lst.remove(user1)

    for otheruser in otherusers_lst:
        corr = cosine_similarity(user1,otheruser)
        if (corr > maximum_correlation):
            maximum_correlation =corr
            maximum_user = otheruser

    print(user1, maximum_user, maximum_correlation)
    return maximum_user


###### Testing Commands ######

def generate_rand_user():
    return random.choice(list(data.keys()))

def test_cosine_similarity(user1="aw548GBK-1XxtSJSqu_OOQ", user2= "O-cosXfQxswcaBr_1bgu-w", random=False):
    if random:
        user1 = generate_rand_user()
        user2 = generate_rand_user()
    return "Cosine Similarity ({0}, {1}) = {2}".format(user1,user2,cosine_similarity(user1, user2))

def test_correlation(user1="aw548GBK-1XxtSJSqu_OOQ", user2= "O-cosXfQxswcaBr_1bgu-w", random=False):
    return correlation(user1, user2)



#distance_method("DhqjO8vmuS30IR8kL-Q6YQ","wZPizeBxMAyOSl0M0zuCjg")
#nearest_with_user("DhqjO8vmuS30IR8kL-Q6YQ")
#recommend_new_restaurant("DhqjO8vmuS30IR8kL-Q6YQ")



