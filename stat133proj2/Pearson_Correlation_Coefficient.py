import ast
with open ('modified_users.txt','r') as inf:
    dict_from_file  = ast.literal_eval(inf.read())

def corrlation(user_id_1,user_id_2):
    n = 0; xy = 0; x = 0; y = 0; sq_y = 0; sq_x = 0
    for business_id in user_id_1["reviews"]:
        if business_id in user_id_2["reviews"]:
            n = n+1
            rating_by_user_1 = user_id_1["reviews"][business_id]["rating"]
            rating_by_user_2 = user_id_2["reviews"][business_id]["rating"]
            x = x + rating_by_user_1
            y = y + rating_by_user_2
            xy = xy + rating_by_user_1*rating_by_user_2
            sq_y = sq_y + rating_by_user_1**2 
            sq_x = sq_x + rating_by_user_2**2
    if n == 0:
        return 'no bussiness id matched'
    else:
        denominator = sqrt(sq_x - (x**2) / n) * sqrt(sq_y -(y**2) / n)
        if denominator == 0:
            return 0
        else:
            corr = (xy -( x * y) / n) / denominator
            #return corr
            return sort(corr)[0]

dk = dict_from_file.keys()
print corrlation(dict_from_file[dk[7]],dict_from_file[dk[2]])
