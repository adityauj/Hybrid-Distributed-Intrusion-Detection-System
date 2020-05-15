from django.shortcuts import render
from django.http import JsonResponse
from collections import Counter
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

import csv
import datetime
import numpy as np
import pandas as pd
import json

from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier




base_path = "/home/rahul/module/bin"


#Read the real-time packet csv file
filename = base_path+'/data/daily/'
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
filename = filename+date+'_Flow.csv'



#Load the classifiers 
decisiontree = joblib.load(base_path+'/decisiontree.sav')
isolationforest = joblib.load(base_path+'/isolationforest.sav')

#this method return http response 
#for test purpose
def index(request):
	return HttpResponse("<h1>Server is online !!</h1>")


#This method returns the IP Address connecte to the system
#Also sends IP Address count,total packet count and packet count for individual packets
#returns JSON data to the server
def getIP(request):
	with open(base_path+filename) as csvfile:
		readCSV = csv.reader(csvfile,delimiter=',')
		ip = []

		for row in readCSV:
			ipAddress = str(row[1])

			ip.append(ipAddress)

		ip_data = dict(Counter(ip))
		ipAddress  = list(ip_data.keys())
		packet_count  = list(ip_data.values())
		total_packets = sum(packet_count)
		ipAddress.pop(0)
		packet_count.pop(0)

	data = {
		"ipAddress" : ipAddress,
		"packet_count" : packet_count,
		"total_packets": total_packets
		}

	return JsonResponse(data)



# method attack() takes POST request 
# used to train the signature module of IDS
# appends the new signature to the dataset and trains the decision tree 
# and IsolationForest 
@csrf_exempt
def attack(request):
	if request.method == 'POST':
		received_data = json.loads(request.body)
		print("Received signature of new attack from MainServer")

		columns = received_data[14]
		received_data = received_data[:14]

		print(received_data)
                
        
		dataFrame = pd.DataFrame(received_data)
		dataFrame = dataFrame.reindex(columns = columns)

		#Read the existing dataset
		dataset = pd.read_csv(base_path+'/reduced.csv',low_memory=False, skipinitialspace=True)
		print("Adding the new Attack signature to the dataset..")
		dataset = pd.concat([dataset,dataFrame],sort=False)
		
		
		dataset.replace({np.nan:'New Attack'}, inplace=True)
		X = dataset.drop('Label',axis=1)
		y = dataset['Label']

		# training DecisionTree and IsolationForest
		print("Training the signature module and anomaly module")
		decisiontree.fit(X,y)
		isolationforest.fit(X)

		# dump the classifiers using joblib.dump()
		joblib.dump(decisiontree,base_path+'/decisiontree.sav')
		joblib.dump(isolationforest,base_path+'/isolationforest')
		
		
		# write the data to the CSV
		dataset.to_csv(base_path+'/reduced.csv',sep=",",index=False)
		print("Signature added sucessfully to the IDS")
		
		return HttpResponse()

	