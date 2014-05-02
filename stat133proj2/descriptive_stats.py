import json
import csv

# businesses from our sample
with open('onlyfood_users.txt', 'rb') as f:
    businesses = {}
    data = json.load(f)
    for user in data.keys():
        for business in data[user]['reviews']:
            city = data[user]['reviews'][business]['city']
            state = data[user]['reviews'][business]['state']
            if business not in businesses:
                businesses[business] = {'city':city, 'state':state}

# get business info from full dataset
with open('data/yelp_academic_dataset.json') as f1:
	data_out = {}
	for line in f1:
		item = json.loads(line)
		if item['type'] == "business":
			business_id = item['business_id']
			if business_id in businesses.keys():
				data_out[business_id] = {'name':item['name'], 
                                         'review_count':item['review_count'], 
                                         'rating':item['stars'], 
                                         'city':businesses[business_id]['city'],
                                         'state':businesses[business_id]['state']
                                         }

# encode business names for csv
for business in data_out.keys():
    name = data_out[business]['name']
    name.encode('utf8')

# write to csv business data
with open('data/business_table.csv', 'w') as f:
    csv_file = csv.writer(f)
    for business in data_out.keys():
        name = data_out[business]['name']
        reviews = data_out[business]['review_count']
        csv_file.writerow([business,
                           name.encode('utf8'),
                           reviews,
                           data_out[business]['rating'],
                           data_out[business]['city'],
                           data_out[business]['state']])

