import numpy as np
import pandas as pd
from sklearn.externals import joblib
from os import sys
from sklearn.ensemble import IsolationForest
import datetime
import requests
import json


server = ["192.168.43.173:8000","192.168.43.219"]
IP = "192.168.43.139:8000"
server


# method to send alert message to the server
def send_alert(message):
    r = requests.post(url = "http://"+server+"/log/logs", json = message)
    if r:
        print("ALERT SEND TO SERVER")
    else:
        print("UNABLE TO CONNECT TO SERVER")







 
np.seterr(divide='ignore', invalid='ignore')

'''
Reading the reduced csv file for processing
'''
dataset = pd.read_csv('reduced.csv', low_memory=False, skipinitialspace=True)
X = dataset.drop('Label', axis=1)
X = X.astype('float64')



'''
Importing decision tree ,featureminmax, isolation Forest , features from 
joblib
'''
decisiontree = joblib.load("decisiontree.pkl")
featureminmax = joblib.load("featureminmax.sav")
features = joblib.load('features.sav')
isolationforest = joblib.load("isolationforest.pkl")

'''
Seting up counters 
'''
signaturecounter = 0
startindex = 0
sflag = 0
aflag = 0
anomalycounter = 0

dtname = 'decisiontree.sav'
ifname = 'isolationforest.sav'
filename = '/home/rahul/module/bin/data/daily/'

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

filename = filename+date+'_Flow.csv'




'''
Rssseal time packets csv file
'''
packets = pd.read_csv(filename, low_memory=False, skipinitialspace=True)

samples = packets

dropping = ['Label']

for f in list(samples.columns):
    if f not in list(features):
        dropping.append(f)

samples.drop(dropping, axis=1, inplace=True)

featureminmax = featureminmax.convert_objects(convert_numeric=True)

for col in list(samples.columns[:-1]):
    
        min_c, max_c = featureminmax.loc[col].values

        n_min=-25
        n_max=25
    
        samples[col]= (((samples[col].values - min_c)/(max_c - min_c))*(n_max - n_min) + n_min)
  
samples.replace({np.nan:'0'}, inplace=True)
current_length = Tot_length = len(samples)
attack = ''








print('Getting In !!')
for index, row in samples.iterrows():
    if((isolationforest.predict([row]))==-1):
        sflag = 0
        print("IN")
        print("Index anomaly",index)
        signaturecounter = 0
        if(aflag == 0):
            startindex = index
            aflag = 1
            
        anomalycounter += 1
        print("anomaly counter : ",anomalycounter)
    else:
        anomalycounter = 0
        aflag = 0
        attack = decisiontree.predict([row])
        if(attack!='BENIGN'):
            print("DTIN")
            print("index is",index)
            if(sflag == 0):
                startindex = index   
                sflag = 1
                
            signaturecounter += 1
            print("signature counter ",signaturecounter)
            
        else:
            print("BENIGN -static")
            signaturecounter = 0
            sflag=0
            
    if(anomalycounter == 15):
        #sending the attack alert to main server
        
        data = {
                "IP" : IP,
                "message" : "NEW ATTACK DETECTED AT SERVER"
        }
        try:
            send_alert(data)
        except:
            print("Oops!",sys.exc_info()[0],"occured.")
            print("Next entry.")
        
        
        print("New Attack performed !! Converting to signature")
        
        
        
        
        attack_signature = samples[startindex:index]
        attack_signature
        
        cols = list(dataset.columns.values)
        attack_signature.to_json("parsed.json", orient = "records", date_format = "epoch", 
                                 double_precision = 10, force_ascii = True, date_unit = "ms",
                                 default_handler = None)
        
        with open('parsed.json') as json_file:  
            signature = json.load(json_file)
        signature.append(cols)
        
        try:
            r = requests.post(url = "http://"+server+"/detect/attack", json = signature)
            if r:
                print("SIGNATURE SEND TO MAIN SERVER")
            else:
                print("FAILED TO SEND SIGNATURE TO MAIN SERVER")
        except:
            print("Unable to connect to server EXCEPTION ",sys.exc_info()[0],"occured")
                
        
        
        
        dataset = pd.concat([dataset,samples[startindex:index]], sort=False)
        dataset.replace({np.nan:'New Attack'}, inplace=True)
        
        #to_test = dataset[dataset['Label'] == 'New Attack']
        
        X = dataset.drop('Label',axis=1)
        y = dataset['Label']
        
        #X = to_test.drop('Label', axis=1)
        #y = to_test['Label']
        decisiontree.fit(X, y) 
        isolationforest.fit(X)
        joblib.dump(decisiontree, dtname)
        joblib.dump(isolationforest, ifname)
        dataset.to_csv("reduced.csv", sep=',', index=False)
        print("Signature added !")
        
    elif(signaturecounter == 15):
        print(attack+" is perfomed !! System compromised ! Shutting down system")
        
        data = {
                "IP" : IP,
                "message" : attack[0]+" performed "
        }
        try:
            send_alert(data)
        except:
            print("Unable to connect to  Main server EXCEPTION ",sys.exc_info()[0],"occured")
            
        sys.exit(0)
print('Getting Out !!')
    





while(True):
    
    samples = pd.read_csv(filename, low_memory=False, skipinitialspace=True)
    samples.drop(dropping, axis=1, inplace=True)
    Tot_length = len(samples)
    
    featureminmax = featureminmax.convert_objects(convert_numeric=True)
    
    if Tot_length != current_length:
        print("In the while !!!")
        for col in list(samples.columns[:-1]):
        
            min_c, max_c = featureminmax.loc[col].values
    
            n_min=-25
            n_max=25
        
            samples[col]= (((samples[col].values - min_c)/(max_c - min_c))*(n_max - n_min) + n_min)

        samples.replace({np.nan:0}, inplace=True)
        
        attack = ''
        
        for index, row in samples[current_length:].iterrows():
            
            
            
            
            
            if(anomalycounter == 15):
                print("New Attack performed !! Converting to signature")
                
                #sending the attack alert to main server
                data = {
                        "IP" : IP,
                        "message" : "NEW ATTACK DETECTED AT SERVER"
                }
                try:
                    send_alert(data)
                except:
                    print("Unable to connect to Main server EXCEPTION ",sys.exc_info()[0],"occured")
                
                print("New Attack performed !! Converting to signature")
                
                
                
                
                attack_signature = samples[startindex:index]
                cols = list(dataset.columns.values)
                attack_signature.to_json("parsed.json", orient = "records", date_format = "epoch", 
                                         double_precision = 10, force_ascii = True, date_unit = "ms",
                                         default_handler = None)
                
                with open('parsed.json') as json_file:  
                    signature = json.load(json_file)
                signature.append(cols)
                
                
                #sending attack signature to the Main Server
                
                try:
                    r = requests.post(url = "http://"+server+"/detect/attack", json = signature)
                    if r:
                        print("SIGNATURE SEND TO MAIN SERVER")
                    else:
                        print("FAILED TO SEND SIGNATURE TO MAIN SERVER")
                except:
                    print("Unable to connect to Main server EXCEPTION ",sys.exc_info()[0],"occured")
                
                
                dataset = pd.concat([dataset,attack_signature], sort=False)
                dataset.replace({np.nan:'New Attack'}, inplace=True)
                X = dataset.drop('Label', axis=1)
                y = dataset['Label']
                decisiontree.fit(X, y) 
                isolationforest.fit(X)
                joblib.dump(decisiontree, dtname)
                joblib.dump(isolationforest, ifname)
                dataset.to_csv("reduced.csv", sep=',', index=False)                
                print("Signature added to this server!")
                
                
            elif(signaturecounter == 15):
                
                print(attack+" is perfomed !! System compromised ! Shutting down system")
                data = {
                "IP" : "192.168.1.1",
                "message" : attack+" performed "
                }
                try:
                    send_alert(data)
                except:
                    print("Unable to connect to Main server EXCEPTION ",sys.exc_info()[0],"occured")

                sys.exit(0)
                
            if((isolationforest.predict([row]))==-1):
                print("In")
                sflag = 0
                signaturecounter = 0
                if(aflag == 0):
                    startindex = index
                    aflag = 1
                    
                anomalycounter += 1
            else:
                anomalycounter = 0
                aflag = 0
                if((decisiontree.predict([row]))!='BENIGN'):
                    print("DTIN")
                    if(sflag == 0):
                        startindex = index   
                        sflagindex = 1
                        
                    signaturecounter += 1
                    attack = decisiontree.predict([row])
                else:
                    print("Benign")
                    signaturecounter = 0
                    sflag=0
    
    current_length=Tot_length