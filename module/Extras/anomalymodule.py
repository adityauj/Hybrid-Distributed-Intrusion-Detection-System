import numpy as np
import pandas as pd
from sklearn.externals import joblib
import datetime

np.seterr(divide='ignore', invalid='ignore')

classifier = joblib.load("isolationforest.sav")
featureminmax = joblib.load("featureminmax.sav")

filename = '/root/module/bin/data/daily/2019-03-29_Flow.csv'

#now = datetime.datetime.now()
#date = now.strftime("%Y-%m-%d")

#filename = filename+date+'_Flow.csv'

dataset2 = pd.read_csv(filename, low_memory=False, skipinitialspace=True)

features = joblib.load('features.sav')

dropping = ['Label']

for f in list(dataset2.columns):
    if f not in list(features):
        dropping.append(f)

dataset2.drop(dropping, axis=1, inplace=True)

featureminmax = featureminmax.convert_objects(convert_numeric=True)

for col in list(dataset2.columns[:-1]):
    
        min_c, max_c = featureminmax.loc[col].values

        n_min=-25
        n_max=25
    
        dataset2[col]= (((dataset2[col].values - min_c)/(max_c - min_c))*(n_max - n_min) + n_min)
  
dataset2.replace({np.nan:'0'}, inplace=True)
current_length = Tot_length = len(dataset2)

print(classifier.predict(dataset2))

while(True):
    
    dataset2 = pd.read_csv(filename, low_memory=False, skipinitialspace=True)
    dataset2.drop(dropping, axis=1, inplace=True)
    Tot_length = len(dataset2)
    
    featureminmax = featureminmax.convert_objects(convert_numeric=True)
    
    if Tot_length != current_length:
        for col in list(dataset2.columns[:-1]):
        
            min_c, max_c = featureminmax.loc[col].values
    
            n_min=-25
            n_max=25
        
            dataset2[col]= (((dataset2[col].values - min_c)/(max_c - min_c))*(n_max - n_min) + n_min)

        dataset2.replace({np.nan:0}, inplace=True)
        print(classifier.predict(dataset2[current_length:]))
        
    current_length=Tot_length
                    
