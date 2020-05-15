import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

np.seterr(divide='ignore', invalid='ignore')

'''
reading dataset
removing the duplicate coloumns
replacing the nan and infinity values with 0
converting Flow_Byts/s and Flow Pkts/s to float64
'''

dataset = pd.read_csv("dataset.csv", low_memory=False,skipinitialspace=True, index_col=False)
dataset = dataset.loc[:,~dataset.columns.str.replace("(\.\d+)$","").duplicated()]
dataset.iloc[:,-1] = dataset.iloc[:,-1].astype('category')

dataset.replace({'Infinity': '0', np.nan:'0'}, inplace=True)

featureminmax = pd.DataFrame(index = dataset.columns,columns=["Min", "Max"])

for col in list(dataset.columns[:-1]):
    
    max_c = dataset[col].max()
    min_c = dataset[col].min()
    
    n_min = -25
    n_max = 25

    featureminmax.loc[col] = (min_c, max_c)
    
    dataset[col]= (((dataset[col].values - min_c)/(max_c - min_c))*(n_max - n_min) + n_min)
    if dataset[col].isnull().values.all() == True:
        dataset.drop(col, axis=1, inplace = True)

dataset.replace({np.nan:0}, inplace=True)


distinct_columns = set()

correlation_data = dataset.corr(method = 'pearson', min_periods = 3).abs().unstack()
correlation_data = correlation_data.sort_values(ascending=False)

list_columns = []
for col_a in dict(correlation_data):
    if correlation_data[col_a] >= 0.99 and correlation_data[col_a] < 1:
        list_columns.append(col_a)

for col1, col2 in list_columns:
    distinct_columns.add(col1)
    distinct_columns.add(col2)

for cols in set(dataset.columns[:-1]):
    if(cols not in distinct_columns):
        dataset.drop(cols, axis=1, inplace = True)

#dataset.drop(["Flow Pkts/s"], axis=1, inplace=True)



X = dataset.drop('Label', axis=1)
y = dataset['Label']


'''
Feature importance 

'''


forest = ExtraTreesClassifier()
forest.fit(X, y)
importances = forest.feature_importances_
#std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
indices = np.argsort(importances)[::-1]

list_columns = []
# Print the feature ranking
for f in range(8,len(dataset.columns)-1):
    
    list_columns.append(dataset.columns[indices[f]])

dataset.drop(list_columns, axis = 1, inplace=True)        
       
features = list(dataset.columns)
joblib.dump(features, 'features.sav')

 
filename = 'featureminmax.sav'
joblib.dump(featureminmax, filename)


dataset.to_csv("reduced.csv", sep=',', index=False)