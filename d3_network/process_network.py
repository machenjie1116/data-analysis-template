import json
import operator
import sets

# get users, and unique user & business id's
def get_data(city, size):
    users = {}
    business_id = []
    with open('../onlyfood_users.txt', 'rb') as infile:
        data = json.load(infile)
        i = 0
        for user in data.keys():
            businesses = data[user]['reviews'].keys()
            user_business = []
            for business in businesses:
                if data[user]['reviews'][business]['city'] == city:
                    if i < size:
                        user_business.append(business)
                        users[user] = user_business
                        if business not in business_id: 
                            business_id.append(business)
                        i += 1
    user_id = users.keys()
    return users, user_id, business_id

# get top-x businesses in a city
def business_topx(top):
    (users, user_id, business_id) = get_data(city, size)
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
    business_ids = {}
    for x in xrange(0,top):
        business_ids[(top_x[x][0])] = top_x[x][1]
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
    return users, user_ids, business_ids


# reindex user id's for displaying
def reid_ids():
    (users, user_ids, business_ids) = business_topx(top)
    user_id = user_ids
    brev_dict = business_ids
    bid_list = business_ids.keys()
    """
    This is the structure we want 
        user_ids = 
        { user_id": {
          "re_id":reindex_id,
          "user_name":user_name,
          "user_reviews":user_reviews
		  "user_match":user_match
		  "rest_recs":rest_recs},...
        }
        business_ids = {business_id: {
          "re_id":reindex_id,
          "bus_name":business_name,
          "bus_reviews":business_reviews},...
        }
    """
    user_ids = {}
    business_ids = {}
    for user in user_id:
        user_ids[user] = {'re_id':'','name':'','reviews':'','user_match':'','rest_recs':''}
    for business in bid_list:
        business_ids[business] = {'re_id':'','name':'','reviews':''}
    # user and business re-index
    for x in xrange(0,len(user_id)):
        user = user_id[x]
        user_ids[user]['re_id'] = x
        
    for x in xrange(0,len(bid_list)):
        business_ids[bid_list[x]]['re_id'] = x + len(user_id)
        
    # user and business name index    
    with open('../data/yelp_academic_dataset.json', 'rb') as f:
        for line in f:
            item = json.loads(line)
            if item['type'] == "user":
                for user in user_id:
                    if item['user_id'] == user:
                        user_ids[user]['name'] = item['name']
            elif item['type'] == "business":
                for business in bid_list:
                    if item['business_id'] == business:
                        business_ids[business]['name'] = item['name']
                        
    # user reviews in sample index
    for user in users.keys():
        user_ids[user]['reviews'] = len(users[user])
                
    for business in bid_list:
        business_ids[business]['reviews'] = brev_dict[business]
                
    return users, user_ids, business_ids

# add user matches and recommendations
def add_usermatch():
    (users, user_ids, business_ids) = reid_ids()
    with open('../data/user_matches.json', 'r') as f1:
        with open('../data/names.json', 'r') as f2:
            data = json.load(f1)
            names = json.load(f2)
            for user1 in data.keys():
                if data[user1]['city'] == city:
                    for user in user_ids.keys():
                        if user1 == user:
                            match_id = data[user1]['user_match']
                            restrec_id = data[user1]['restaraunt_recs']
                            user_ids[user]['user_match'] = names[match_id]
                            user_ids[user]['rest_recs'] = names[restrec_id]
    return users, user_ids, business_ids


# create nodes for each user and business, sized by review count
def create_nodes():
    (users, user_ids, business_ids) = add_usermatch()
    nodes = []
    for user in user_ids.keys():
        nodes.append({"_name":user_ids[user]['name'], "user_reviewcount":user_ids[user]['reviews'],"user_match":user_ids[user]['user_match'],"rest_recs":user_ids[user]['rest_recs']})
    for business in business_ids.keys():
        nodes.append({"_name":business_ids[business]['name'], "bus_reviewcount":business_ids[business]['reviews']})
    return nodes

# create links from user to businesses, business network links
def bus_links():
    (users, user_ids, business_ids) = reid_ids()
    links = []
    for user in users.keys():
        for business in users[user]:
            links.append({"source": user_ids[user]['re_id'], "target": business_ids[business]['re_id']})
    return links

# user network links
def user_links():
    links = []
    for user_1 in user_ids.keys():
        for user_2 in user_ids.keys():
                user1_bus = set(users[user_1])
                user2_bus = set(users[user_2])
                if len(user1_bus.intersection(user2_bus)) > 0:
                    links.append({"source":user_ids[user_1]['re_id'], "target":user_ids[user_2]['re_id']})
    return links

def main():
	global size; global city; global top
	size = raw_input('Size of sample: ')
	city = raw_input('City: ')
	outname = raw_input('Output file name: ')
	top = int(raw_input('Top # businesses: '))
	bus_user = raw_input('Business or User graph? ')
	if bus_user == "Business" or bus_user == "Bus" or bus_user == "business" or bus_user == "bus":
		new_data = {"nodes":create_nodes(), "edges":bus_links()}
	elif bus_user == "User" or bus_user == "user":
		new_data = {"node":create_nodes(), "edges":user_links()}
	with open('data/' + outname, 'w') as outfile:
		json.dump(new_data, outfile, indent=2)

if __name__=='__main__':
	main()

