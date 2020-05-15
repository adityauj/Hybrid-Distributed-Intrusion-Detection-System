import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dataset = pd.read_csv("dataset.csv",low_memory=False,skipinitialspace=True)
dataset = dataset.loc[:,~dataset.columns.str.replace("(\.\d+)$","").duplicated()]
dataset.iloc[:,-1] = dataset.iloc[:,-1].astype('category')
dataset.replace({'Infinity': '0', np.nan:'0'}, inplace=True)

dataset['Flow Bytes/s'] = dataset['Flow Bytes/s'].str.replace('','').astype(np.float64)
dataset['Flow Packets/s'] = dataset['Flow Packets/s'].str.replace('','').astype(np.float64)
 
X = dataset.drop('Label', axis=1)
y = dataset['Label'] 

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,random_state = 1)

from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)




