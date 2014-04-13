import random
import json
from math import sqrt

with open('modified_users.txt','r') as inf:
    dict_from_file = json.load(inf)
    data = dict_from_file

def get_business_ids(user_id):
    """returns a dictionary of {business_id: {"rating": NA, "state": NA, "city": NA}} """
    return data[user_id]["reviews"] 

def get_rating(user_id,business_id):
    return data[user_id]["reviews"][business_id]["rating"]

def distance_method(user_id1, user_id2, r):
    distance = 0
    common_rating = False
    user1_business_ids = get_business_ids(user_id1)
    user2_business_ids = get_business_ids(user_id2)

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
        neighbor_reviews = get_business_ids(neighbor)
        user_reviews = get_business_ids(user_id1)

    elif method == 'euclidean':
        neighbor = nearest_with_user(user_id1,2)
        neighbor_reviews = get_business_ids(neighbor)
        user_reviews = get_business_ids(user_id1)

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
   


"""
def pearson(user_id1,user_id2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    user1_business_ids = get_business_ids(user_id1)
    user2_business_ids = get_business_ids(user_id2)

    for business_id in list(user1_business_ids.keys()):
        if business_id in list(user2_business_ids.keys()):
            n += 1
            x = get_rating(user_id1,business_id)
            y = get_rating(user_id2,business_id)
            sum_xy += x*y
            sum_x += x
            sum_y += y
            sum_x2 += x**2
            sum_y2 += y**2

    denominator = sqrt(sum_x2 - (sum_x**2) / n) * sqrt(sum_y2 - (sum_y**2) / n)

    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y)/n)/denominator"""







###### Testing Commands ######

def generate_rand_user():
    return random.choice(list(data.keys()))





#distance_method("DhqjO8vmuS30IR8kL-Q6YQ","wZPizeBxMAyOSl0M0zuCjg")
#nearest_with_user("DhqjO8vmuS30IR8kL-Q6YQ")
#recommend_new_restaurant("DhqjO8vmuS30IR8kL-Q6YQ")



