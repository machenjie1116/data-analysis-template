from recommend import *
import numpy as np
from multiprocessing import Pool
import time
import json

def chunks(l, n):
    if n<1:
        n=1
    return [l[i:i+n] for i in range(0, len(l), n)]

MSE = {}
def combine_results(result):
	MSE.update(result)
	
	
def mse_all_users(method):
    output_file = "./processed_data/" + method + "_error.txt"
    users_chunked = chunks(data.keys(), 50)
    pool = Pool()
    
    for users_chunk in users_chunked:
        pool.apply_async(mse_subset_users, args=(method, users_chunk), callback=combine_results)
    pool.close()
    pool.join()
    with open(output_file, "w") as outfile:
        json.dump(MSE, outfile, indent=4)
        	
"""    
def mse_all_users(method):
    users = data.keys()[:60]
    pool = Pool()

    args = []
	#Split 42052 users into 106 groups of 400 each
    users_split = chunks(users, 14)
    for chunk in users_split:
        args.append([method, chunk])
    
    print "Args", args
    return pool.map_async(mse_subset_users, args)
"""

def mse_subset_users(method, users):
    curr_time = time.time()
    MSE = {}
    for user in users:
        MSE[user] = test_recommendations(user, method)
    total_time = time.time() - curr_time
    print total_time, "Avg Time per User = {0}".format(total_time / len(users))
    return MSE


"""
Computes error for user.
The error is defined as the average of all the absolute
differences between predicted rating for the restaurants and the actual rating.
"""
def test_recommendations(user, method):
    #print user
    if (method not in ["manhattan", "euclidean", "cosine"]):
        #print "Method: ", method
        raise Exception("Invalid Method")

    if len(data[user]["reviews"].keys()) <= 1:
        return np.nan

    predicted_ratings = []
    actual_ratings = []

    if (method == "cosine"):
        user_businesses = data[user]["reviews"].keys()
        for business_id in user_businesses:
            #store the data we are about to delete
            temp = data[user]["reviews"][business_id]
            #pretend like this user never went to the business in the first place
            del data[user]["reviews"][business_id]

            closest_users = highest_cosine_user(user)

            if closest_users.has_key(0.0):
                del closest_users[0.0] #remove users which don't have any correlation with target user

            predicted_rating = get_predicted_rating(business_id, closest_users, sorted(closest_users.keys(), reverse = True))
            #restore the ignored/deleted review
            data[user]["reviews"][business_id] = temp

            if (predicted_rating != None):
                predicted_ratings.append(predicted_rating)
                actual_ratings.append(data[user]["reviews"][business_id]["rating"])


        assert (len(actual_ratings) == len(predicted_ratings))
        actual_ratings = np.array(actual_ratings)
        predicted_ratings = np.array(predicted_ratings)
        n = len(actual_ratings)
        #return mean squared error of (actual ratings - predicted ratings)
        errors = actual_ratings - predicted_ratings
        rms_error = np.sqrt(float(np.sum(np.square(errors)) / n))
        return rms_error

    elif ((method == "manhattan") or (method == "euclidean")):
        r = {"manhattan":1, "euclidean":2}[method]
        user_businesses = data[user]["reviews"].keys()
        for business_id in user_businesses:
            #store the data we are about to delete
            temp = data[user]["reviews"][business_id]
            #pretend like this user went to the business in the first place by deleting the review
            del data[user]["reviews"][business_id]
            closest_users = nearest_with_user(user, r)
            if closest_users.has_key(MAX_INT):
                del closest_users[MAX_INT]

            predicted_rating = get_predicted_rating(business_id, closest_users, sorted(closest_users.keys()))
            #restore the ignored/deleted review
            data[user]["reviews"][business_id] = temp

            if (predicted_rating != None):
                predicted_ratings.append(predicted_rating)
                actual_ratings.append(data[user]["reviews"][business_id]["rating"])


        assert (len(actual_ratings) == len(predicted_ratings))
        actual_ratings = np.array(actual_ratings)
        predicted_ratings = np.array(predicted_ratings)
        n = len(actual_ratings)
        #return mean squared error of (actual ratings - predicted ratings)
        errors = actual_ratings - predicted_ratings
        rms_error = np.sqrt( float(np.sum(np.square(errors)) / n))
        return rms_error


def get_predicted_rating(business_id, closest_users, correlations):
    for corr in correlations:
        corr_users = closest_users[corr]
        for corr_user in corr_users:
            if business_id in data[corr_user]["reviews"].keys():
                predicted_rating = data[corr_user]["reviews"][business_id]["rating"]
                return predicted_rating
def main():
    mse_all_users("manhattan")

if __name__ == '__main__':
    main()
