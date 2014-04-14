

def is_food_related(business):
    categories = ["Food", "Restaturants", "Buffets", "Creperies", "Juice Bars & Smoothies", "Candy Stores", "Diners"]


def read_yelpdata(location = r'./yelp_academic_dataset/yelp_rawdata'):
    businesses = {}
    users = {}

    with open(location, 'rb') as infile:
        for line in infile:
            item = json.loads(line)
            if item['type'] == 'business':
				if is_food_related(item):
					businesses['business_id'] = {"city":item['city'], "state":item["state"]}
            elif item['type'] == 'review':
                business_id = item['business_id']
                user_id = item['user_id']
                rating = item['stars']
                if users.has_key(user_id):
                    users[user_id][business_id] = rating
                else:
                    users[user_id] = {}
                    users[user_id][business_id] = rating
            elif item['type'] == 'user':
                pass
            else:
                #should never trigger
                raise ValueError("Unknown type")
        return users, businesses

def process_data1(users, businesses):
	return users
	"""
	for user in users.keys():
		reviewsbyuser = users[user]
		business_ids = reviewsbyuser.keys()
		for business_id in business_ids:
			if businesses.has_key(business_id):
				city = businesses[business_id]["city"]
				state = businesses[business_id]["state"]
				curr_rating = users[user][business_id]
				users[user][business_id] = [curr_rating, city, state]
			else:
				curr_rating = users[user][business_id]
				users[user][business_id] = [curr_rating, "NA", "NA"]
	return users
	"""




import json
def main():
    (users, businesses) = read_yelpdata()
    users = process_data1(users, businesses)
    print "Processed ", len(users.keys()), "users"
    with open('./processed_data/users.txt', 'w') as outfile:
        json.dump(users, outfile, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()

