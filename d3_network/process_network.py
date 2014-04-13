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
        nodes.append({"person":business, "reviewcount":len(business_reviews[i])})
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

if __init__=='__main__":
	main()

