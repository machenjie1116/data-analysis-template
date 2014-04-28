from testing_framework import *
import csv

csv_out = open("errors.csv",'w')
mywriter = csv.writer(csv_out)

mywriter.writerow(mse_subset_users('cosine'))
csv_out.close()