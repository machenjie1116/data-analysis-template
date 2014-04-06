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
	  return response["location"]


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


def compute_user_locations_helper(users):
	return users

def compute_user_locations():
    users_file = "./processed_data/users.txt"
    businesses_file = "./processed_data/businesses.txt"
    modified_users_output = "./processed_data/modified_users.txt"
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
    with open(modified_users_output, 'w') as outfile:
        json.dump(users, outfile, indent=4)



def main():
	compute_user_locations()
	pass

if __name__ == '__main__':
    main()
