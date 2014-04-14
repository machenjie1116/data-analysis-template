import json
from math import sqrt
with open ('modified_users.txt','r') as inf:
    dict_from_file  = json.load(inf)

def correlation(user_id_1,user_id_2):
    n = 0; xy = 0; x = 0; y = 0; sq_y = 0; sq_x = 0
    for business_id in dict_from_file[user_id_1]["reviews"]:
        if business_id in dict_from_file[user_id_2]["reviews"]:
            n = n+1
            rating_by_user_1 = dict_from_file[user_id_1]["reviews"][business_id]["rating"]
            rating_by_user_2 = dict_from_file[user_id_2]["reviews"][business_id]["rating"]
            x = x + rating_by_user_1
            y = y + rating_by_user_2
            xy = xy + rating_by_user_1*rating_by_user_2
            sq_y = sq_y + rating_by_user_1**2
            sq_x = sq_x + rating_by_user_2**2
    if n == 0:
        return 'no bussiness id matched'
    else:
        print sq_x, x, sq_y, y, n
        denominator = sqrt(abs(sq_x - float((x**2) / n))) * sqrt(abs(sq_y - float((y**2) / n)))
        if denominator == 0:
            return 0
        else:
            print "xy" ,xy, "x", x, "y", y, "denominator", denominator
            corr = (xy -( x * y) / n) / denominator
            return corr

def cosine_similarity(user_1, user_2):
    business1 = dict_from_file[user_1]["reviews"].keys()
    business2 = dict_from_file[user_2]["reviews"].keys()
    print business1, business2
    business1.extend(business2)
    businesses = set(business1)
    ratings_1 = []
    ratings_2 = []
    for business in businesses:
        if dict_from_file[user_1]["reviews"].has_key(business):
            ratings_1.append()






def test_cosine_similarity(user1="aw548GBK-1XxtSJSqu_OOQ", user2= "O-cosXfQxswcaBr_1bgu-w"):
    return cosine_similarity(user1, user2)
def test_correlation(user1="aw548GBK-1XxtSJSqu_OOQ", user2= "O-cosXfQxswcaBr_1bgu-w"):
    return correlation(user1, user2)
#dk = dict_from_file.keys()
#print corrlation(dict_from_file[dk[7]],dict_from_file[dk[2]])