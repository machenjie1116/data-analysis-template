from recommend import *
import numpy as np


def mse_all_users():
    users = data.keys()
    users = users[:30]
    MSE = []
    for user in users:
        MSE.append(test_recommendations(user, "cosine"))
    MSE = np.array(MSE)
    MSE = MSE[~np.isnan(MSE)]
    return MSE

"""
Computes error for user.
The error is defined as the average of all the absolute
differences between predicted rating for the restaurants and the actual rating.
"""
def test_recommendations(user, method):
    if (method not in ["manhattan", "euclidean", "cosine"]):
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
        rms_error = np.sqrt( float(np.sum(np.square(errors)) / n))
        return float(np.linalg.norm(errors, 2)/ n), rms_error

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
        return float(np.linalg.norm(errors, 2)/ n), rms_error


def get_predicted_rating(business_id, closest_users, correlations):
    for corr in correlations:
        corr_users = closest_users[corr]
        for corr_user in corr_users:
            if business_id in data[corr_user]["reviews"].keys():
                predicted_rating = data[corr_user]["reviews"][business_id]["rating"]
                return predicted_rating
def main():
    n = 100000
    errors = np.array([4]*n)
    print np.sqrt(float(np.sum(np.square(errors)) / n))

if __name__ == '__main__':
    main()
