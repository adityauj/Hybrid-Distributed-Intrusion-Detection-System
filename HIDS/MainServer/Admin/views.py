import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import csv
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier

import datetime



# servers registered to the MainServer
servers = ['192.168.43.139:8000','192.168.43.219:8000']


#base path to the IDS module
base_path = '/home/rahul/module/bin'

#Load the classifiers 
decisiontree = joblib.load(base_path+'/decisiontree.sav')
isolationforest = joblib.load(base_path+'/isolationforest.sav')


# index() returns the index.html page
# dashboard page with all the network information
def index(request):
	return render(request,'Admin/index.html')


# writing the sequence of events of .txt file
def write_to_file(message):
	

	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")

	file_data = open(base_path+"/logs.txt","a+")

	data_to_file = date+" "+message+"\n"
	file_data.write(data_to_file)

	file_data.close()


#  method sends GET request to the servers[] and gets
#  the IP addresses , total packets , and all IPs connected to the 
#  server 	
def home(request):
	
	total = {}
	length = len(servers)

	
	for i in range(length):
		url = "http://"+servers[i]+"/getIP/ip"	 
		r = requests.get(url)
		
		data = r.json()
		total[servers[i]] = data 
		

	return JsonResponse(total)



# getTextFile() reads the log file on MainServer and 
# returns the contents of the log file.
def getTextFile(request):
	f=open(base_path+"/logs.txt", "r")
	if f.mode == 'r':
		contents =f.read()

	data={
		"content" : contents
	}
	return JsonResponse(data)



# doughnut_data() opens the dataset.csv file and 
# returns different attacks and their count
def doughnut_data(request):
	with open(base_path+'/reduced.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=",")
	    attacks = []

	    for row in readCSV:
	        attack = row[8]
	        attacks.append(attack)

	    attack_data = dict(Counter(attacks))
	    attack_labels = list(attack_data.keys())
	    attack_count = list(attack_data.values())

	    attack_labels.pop(0)
	    attack_count.pop(0)
		
	data ={
		"attack_labels" : attack_labels,
		"attack_count" : attack_count
	}
	return JsonResponse(data)



# attack () - receives POST request from other servers
# Performs following steps
# 1. Receive the New Attack signature (POST request)
# 2. Send the signature to other servers (servers[])
# 3. Train the signature module of MainServer
# 4. Write the new signature to the dataset and save in .csv format

@csrf_exempt
def attack(request):
	if request.method == 'POST':
		received_data = json.loads(request.body)
		
		print("Sending request to connected servers")
		message = "Sending attack signature to connected servers"
		write_to_file(message)
		for i in range(len(servers)):
			URL = "http://"+servers[i]+"/detect/attack"

			print("Sending attack signature to "+URL+"...")
			message = "SENDING ATTACK SIGNATURE TO"+URL+"..."
			write_to_file(message)
			r = requests.post(url = URL, json = received_data)
			
			if r:
				print("Attack signature  sucessfully send to server "+URL)
				message = "SIGNATURE SEND TO SERVER "+URL
				write_to_file(message)
			else:
				print("FAILED TO SEND SIGNATURE TO SERVER "+URL)
				message = "FAILED TO SEND SIGNATURE TO SERVER "+URL
				write_to_file(message)

		print(received_data[14])
		columns = received_data[14]
		received_data = received_data[:14]


		dataFrame = pd.DataFrame(received_data)
		dataFrame = dataFrame.reindex(columns = columns)

		#Read the exiting dataset
		dataset = pd.read_csv(base_path+'/reduced.csv',low_memory=False, skipinitialspace=True)
		
		print("Appending the signature to the dataset")
		dataset = pd.concat([dataset,dataFrame],sort=False)
		
		
		dataset.replace({np.nan:'New Attack'}, inplace=True)
		X = dataset.drop('Label',axis=1)
		y = dataset['Label']

		decisiontree.fit(X,y)
		isolationforest.fit(X)

		joblib.dump(decisiontree,base_path+'/decisiontree.sav')
		joblib.dump(isolationforest,base_path+'/isolationforest.sav')
		
		
		#dataset.to_csv(base_path+'/reduced.csv',sep=",",index=False)
		print("Signature sucessfully added to MainServer")
		message = "SIGNATURE SUCESSFULLY ADDED TO MAIN SERVER"
		write_to_file(message)
		
		return HttpResponse()


# writes the sequence of events to .txt file 
@csrf_exempt
def write_logs(request):
	if request.method=='POST':
		
		received_json_data=json.loads(request.body)
		
		message = received_json_data['message']+" "+received_json_data['IP']
		#static writing to file
		write_to_file(message)

		return HttpResponse()



