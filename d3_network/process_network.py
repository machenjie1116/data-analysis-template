import json
import operator

# get users, and unique user & business id's
def get_data():
    users = {}
    business_id = []
    with open('../stat133proj2/processed_data/onlyfood_users.txt', 'rb') as infile:
        data = json.load(infile)
        for user in data.keys():
            businesses = data[user]['reviews'].keys()
            user_business = []
            for business in businesses:
                if data[user]['reviews'][business]['city'] == "Berkeley":
                    user_business.append(business)
                    users[user] = user_business
                    if business not in business_id: 
                        business_id.append(business)
    user_id = users.keys()
    return users, user_id, business_id

# get top-x businesses in a city
def business_topx():
    top = 5
    (users, user_id, business_id) = get_data()
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
    (users, user_ids, business_ids) = business_topx()
    user_id = user_ids
    brev_dict = business_ids
    bid_list = business_ids.keys()
    """
    This is the structure we want 
        user_ids = 
        { user_id":
          "re_id":reindex_id,
          "user_name":user_name,
          "user_reviews":user_reviews},...
        }
        business_ids = 
        { business_id:
          "re_id":reindex_id,
          "bus_name":business_name
          "bus_reviews":business_reviews},...
        }
    """
    user_ids = {}
    business_ids = {}
    for user in user_id:
        user_ids[user] = {'re_id':'','name':'','reviews':''}
    for business in bid_list:
        business_ids[business] = {'re_id':'','name':'','reviews':''}
    # user and business re-index
    for x in xrange(0,len(user_id)):
        user = user_id[x]
        user_ids[user]['re_id'] = x
        
    for x in xrange(0,len(bid_list)):
        business_ids[bid_list[x]]['re_id'] = x + len(user_id)
        
    # user and business name index    
    with open('data/yelp_academic_dataset.json', 'rb') as f:
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

# create nodes for each user and business, sized by review count
def create_nodes():
    (users, user_ids, business_ids) = reid_ids()
    nodes = []
    for user in user_ids.keys():
        nodes.append({"_name":user_ids[user]['name'], "user_reviewcount":user_ids[user]['reviews']})
    i = 0 
    for business in business_ids.keys():
        nodes.append({"_name":business_ids[business]['name'], "bus_reviewcount":business_ids[business]['reviews']/10})
        i += 1
    return nodes

# create links from user to businesses
def create_links():
    (users, user_ids, business_ids) = reid_ids()
    links = []
    for user in users.keys():
        for business in users[user]:
            links.append({"source": user_ids[user]['re_id'], "target": business_ids[business]['re_id']})
    return links

def main():
	new_data = {"nodes":create_nodes(), "edges":create_links()}
	with open('data/Berkeley.json', 'w') as outfile:
		json.dump(new_data, outfile, indent=2)

if __name__=='__main__':
	main()

