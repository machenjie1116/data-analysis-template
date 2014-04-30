import recommend, json, sys
from multiprocessing import Pool
def chunks(l, n):
    if n<1:
        n=1
    return [l[i:i+n] for i in range(0, len(l), n)]

def read_userlist(file_loc = r"./processed_data/user_list.json"):
    with open(file_loc, "rb") as inputFile:
        user_list = json.load(inputFile)
    return user_list

user_matches = {}

def combine_results(result):
    user_matches.update(result)

def user_matches_all(full_user_list, output):
    users_chunked = chunks(full_user_list.keys(), 50)

    pool = Pool()

    for user_chunk in users_chunked:
        pool.apply_async(user_matches_subset, args = (user_chunk, full_user_list), callback=combine_results)
    pool.close()
    pool.join()
    with open(output, "w") as outputFile:
        json.dump(user_matches, outputFile, indent=4)

def user_matches_subset(user_list, full_user_list):
    curr_time = time.time()
    print "starting new batch"
    sys.stdout.flush()
    returnVal = {}
    for user in user_list:
        city = full_user_list[user]["city"]

        recommendation = recommend.recommend_new_restaurant_2(user, "cosine")[0]
        restaraunt_id = recommendation[0]
        restaraunt_name = recommendation[1]
        user_match = recommendation[2]
        predicted_rating = recommendation[3]
        correlation = recommendation[4]
        returnVal[user] = {"city":city, "user_match":user_match, "restaraunt_recs":restaraunt_id}
    total_time = time.time() - curr_time
    print "Took {0} seconds".format(total_time)
    sys.stdout.flush()
    return returnVal

def main():
    output = r"./processed_data/user_matches.json"
    user_list = read_userlist()
    user_matches_all(user_list, output)

if __name__ == '__main__':
    main()
