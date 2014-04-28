from testing_framework import *
import csv
import numpy

csv_out = open("nperror.csv",'w')

array = mse_subset_users('cosine')
numpy.savetxt("nperror.csv",array,delimiter=",")

csv_out.close()