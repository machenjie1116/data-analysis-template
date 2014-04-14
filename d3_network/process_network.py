import json
import operator

# get users, and unique user & business id's
def get_data():
    users = {}
    business_ids = []
    with open('modified_users.txt', 'rb') as infile:
        data = json.load(infile)
        for user in data.keys():
            businesses = data[user]['reviews'].keys()
            user_business = []
            for business in businesses:
                if data[user]['reviews'][business]['city'] == "Berkeley":
                    user_business.append(business)
                    users[user] = user_business
                    if business not in business_ids: 
                        business_ids.append(business)
    user_ids = users.keys()
    return users, user_ids, business_ids

# get top-x businesses in a city
def business_topx():
    top = 1
    (users, user_ids, business_ids) = get_data()
    businesses = []
    business_count = {}
    for user in users.keys():     
        for business in users[user]:
            businesses.append(business)
    #count business occurances, sort by most reviews
    for business in businesses:
        if business not in business_count.keys():
            business_count[business] = businesses.count(business)
    sorted_x = sorted(business_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    top_x = sorted_x[0:top]
    business_ids = []; business_reviews = []
    for x in xrange(0,top):
        business_ids.append(top_x[x][0])
        business_reviews.append(top_x[x][1])
    # filter out non-top reviews from users    
    new_users = {}
    for user in users.keys():
        user_biz = []
        for business in users[user]:
            if business in business_ids:
                user_biz.append(business)
                new_users[user] = user_biz
    users = new_users
    user_ids = users.keys()
    return users, user_ids, business_ids, business_reviews


# reindex user id's for displaying
def reid_ids():
    (users, user_ids, business_ids, business_reviews) = business_topx()
    user_dict = {}
    for x in xrange(0,len(user_ids)):
        user_dict[user_ids[x]] = x
        user_ids[x] = x
    business_dict = {}
    for x in xrange(0,len(business_ids)):
        business_dict[business_ids[x]] = x + len(user_ids)
        business_ids[x] = x + len(user_ids)
    for user in users.keys():
        for i,j in user_dict.iteritems():
            if user == i: users[j] = users.pop(user)    
	# replace business items 
    for user in users.keys():
        for y in xrange(0,len(users[user])):
            for i,j  in business_dict.iteritems():
                if users[user][y] == i: users[user][y] = j
    return users, user_ids, business_ids, business_reviews

# create nodes for each user and business, sized by review count
def create_nodes():
    nodes = []
    (users, user_ids, business_ids, business_reviews) = reid_ids()
    for user in user_ids:
        nodes.append({"person":user, "reviewcount":len(users[user])})
    i = 0 
    for business in business_ids:
        nodes.append({"person":business, "reviewcount":business_reviews[i]})
        i += 1
    return nodes

# create links from user to businesses
def create_links():
    links = []
    (users, user_ids, business_ids, business_reviews) = reid_ids()
    for user in user_ids:
        for business in users[user]:
            links.append({"source": user, "target": business})
    return links

def main():
	new_data = {"nodes":create_nodes(), "edges":create_links()}
	with open('data.json', 'w') as outfile:
		json.dump(new_data, outfile, indent=2)

if __name__=='__main__':
	main()
