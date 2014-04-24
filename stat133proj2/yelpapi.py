import json
import oauth2
import optparse
import urllib
import urllib2
import time
import os



def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  #print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
  #print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  if response.has_key("error"):
	  return 0
  else:
	  return response


def get_business_locations():
	start_time = time.time()
	host = "api.yelp.com"
	base_path = "/v2/business/"
	url_params = {}
	consumer_key = "hdFjqcPRZyZ0eqi26af3tw"
	consumer_secret = "Ex5U5ZJflQb-tx4T0AJiyKKf1yM"
	token = "-w0vkTLODYebA_4PrEer9T48bHB_TD1S"
	token_secret = "PZnOemFP0TJbkzLKQsBn8lNO3U8"
	location =  "./processed_data/users.txt"
	outputFile = "./processed_data/businesses.txt"

	businesses = {}
	with open(location, 'rb') as infile:
		users = json.load(infile)
		users_processed = 0
		for user in users.keys():
			users_processed += 1
			reviews = users[user]
			business_ids = reviews.keys()
			for business_id in business_ids:
				if (not businesses.has_key(business_id)):
					businesses[business_id] = {}
				else:
					pass


	print "Finished getting list of", len(businesses.keys()), "businesses"
	for business_id in businesses.keys():
		path = base_path + business_id
		response = request(host, path, url_params, consumer_key, consumer_secret, token, token_secret)
		try:
			if (response != 0):
				city = response["city"]
				state = response["state_code"]
			else:
				city = "NA"
				state = "NA"
			businesses[business_id]["city"] = city
			businesses[business_id]["state"] =  state
		except KeyError:
			print "Failed : ", business_id
	with open(outputFile, 'w') as outfile:
		json.dump(businesses, outfile, indent=4)
	elapsed_time = time.time() - start_time
	print "Elapsed Time: ", elapsed_time, " s"

import operator
def compute_user_locations():
    users_file = "./processed_data/users.txt"
    businesses_file = "./processed_data/businesses.txt"
    businesses = {}
    with open(businesses_file, 'rb') as infile:
        businesses = json.load(infile)
    with open(users_file, 'rb') as infile:
        users = json.load(infile)
    for user in users.keys():
        if (user == "-1J99GAWYAbK7sbZcVEgxQ"):
            print users[user]
        review = {}
        for business_id in users[user].keys():
            city = businesses[business_id]["city"]
            state = businesses[business_id]["state"]
            rating = users[user][business_id]
            #users[user][business_id] = {"rating":rating, "city":city, "state":state}
            review[business_id] = {"rating":rating, "city":city, "state":state}
        users[user]["reviews"] = review


    for user in users.keys():
        for key in users[user].keys():
            if (key != "reviews"):
                del users[user][key]
    user_locations = {}
    for user in users.keys():
        location_count = {}
        for business in users[user]["reviews"].keys():
            business_location = users[user]["reviews"][business]["city"]
            if location_count.has_key(business_location):
                location_count[business_location] += 1
            else:
                location_count[business_location] = 1
        location = max(location_count.iteritems(), key=operator.itemgetter(1))[0]
        user_locations[user] = location

    for user in users:
        users[user]["location"] = user_locations[user]
    return users

def read_yelpdata(location = r'./yelp_academic_dataset/yelp_rawdata'):
    businesses = []
    with open(location, 'rb') as infile:
        for line in infile:
            item = json.loads(line)
            if item['type'] == 'business':
                if is_food_related(item):
                    businesses.append(item["business_id"])
    return businesses

def is_food_related(business):
    categories = ["Food", "Restaturants", "Buffets", "Creperies", "Juice Bars & Smoothies", "Candy Stores", "Diners"]
    for x in categories:
        if x in business["categories"]:
            return True
    return False

def filter_businesses(users, businesses):
    for user in users.keys():
        for business_id in users[user]["reviews"].keys():
            if (business_id not in businesses):
                del users[user]["reviews"][business_id]
        if users[user]["reviews"] == {}:
            del users[user]
    return users


def get_business_info(business_id):
    host = "api.yelp.com"
    base_path = "/v2/business/"
    url_params = {}
    consumer_key = "hdFjqcPRZyZ0eqi26af3tw"
    consumer_secret = "Ex5U5ZJflQb-tx4T0AJiyKKf1yM"
    token = "-w0vkTLODYebA_4PrEer9T48bHB_TD1S"
    token_secret = "PZnOemFP0TJbkzLKQsBn8lNO3U8"
    path = base_path + business_id
    response = request(host, path, url_params, consumer_key, consumer_secret, token, token_secret)
    try:
        if response.has_key("error"):
            return (None, None)
    except:
        print response, business_id
        return (None, None)
    else:
		return (response["categories"], response["name"])


def main():
    users_input = "./processed_data/onlyfood_users.txt"
    users_output = "./processed_data/name_category_users.txt"
    
    with open(users_input, 'rb') as infile:
        data = json.load(infile)
    business_ids = []
    for user in data.keys():
        for business_id in data[user]["reviews"]:
            business_ids.append(business_id)

    business_ids = list(set(business_ids))
    
    total = float(len(business_ids))
    business_info = {}
    count = 0
    for business_id in business_ids:
        (categs, name) = get_business_info(business_id)
        if (categs):
            categories = [x[0] for x in categs]
        else:
            categories = None
        business_info[business_id] = (name,  categories)
        count += 1
        if ((count % 100) == 0):
            print "{0} / {1} businesses retreived".format(count, total)

    for user in data.keys():
        for business_id in data[user]["reviews"]:
            name, categories = business_info[business_id]
            data[user]["reviews"][business_id]["categories"] = categories
            data[user]["reviews"][business_id]["name"] = name
    with open(users_output, "w") as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    main()
