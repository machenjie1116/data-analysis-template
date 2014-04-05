


def read_yelpdata(location = r'/home/harish/stat133proj2/yelp_academic_dataset/yelp_rawdata'):
    restaurants = []
    reviews = []
    users = {}

    with open(location, 'rb') as infile:
        for line in infile:
            item = json.loads(line)
            if item['type'] == 'business':
                pass
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
        return users

def process_data1(users):
    with open('test.txt', 'w') as outfile:
        json.dump(users, outfile, indent=4, sort_keys=True)








import json
def main():
    process_data1(read_yelpdata())

if __name__ == '__main__':
    main()

