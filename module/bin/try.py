import numpy as np
import pandas as pd
from sklearn.externals import joblib
from os import sys
from sklearn.ensemble import IsolationForest
import datetime

np.seterr(divide='ignore', invalid='ignore')


# Reading dataset
dataset = pd.read_csv('reduced.csv', low_memory=False, skipinitialspace=True)
X = dataset.drop('Label', axis=1)
X = X.astype('float64')


decisiontree = joblib.load("decisiontree.sav")
featureminmax = joblib.load("featureminmax.sav")
features = joblib.load('features.sav')
isolationforest = joblib.load("isolationforest.sav")

signaturecounter = 0
startindex = 0
sflag = 0
aflag = 0
anomalycounter = 0

dtname = 'decisiontree.sav'
ifname = 'isolationforest.sav'
filename = '/home/rahul/module/bin/data/daily/2019-04-04_Flow.csv'


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
            print('While loop')
            if(anomalycounter == 15):
                print("New Attack performed !! Converting to signature :) ")
                dataset = pd.concat([dataset,samples[startindex:index]], sort=False)
                dataset.replace({np.nan:'New Attack'}, inplace=True)
                X = dataset.drop('Label', axis=1)
                y = dataset['Label']
                decisiontree.fit(X, y) 
                isolationforest.fit(X)
                joblib.dump(decisiontree, dtname)
                joblib.dump(isolationforest, ifname)
                dataset.to_csv("reduced.csv", sep=',', index=False)                
                print("Signature added !")
                
            elif(signaturecounter == 15):
                print(attack+" is perfomed !! System compromised ! Shutting down system")
                sys.exit(0)
                
            if((isolationforest.predict([row]))==-1):
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
                    if(sflag == 0):
                        startindex = index   
                        sflagindex = 1
                        
                    signaturecounter += 1
                    attack = decisiontree.predict([row])
                else:
                    signaturecounter = 0
                    sflag=0
    
    current_length=Tot_length

