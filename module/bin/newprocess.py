import numpy as np
import pandas as pd

np.seterr(divide='ignore', invalid='ignore')

dataset = pd.read_csv("NewData.csv",low_memory=False,skipinitialspace=True)
dataset = dataset.loc[:,~dataset.columns.str.replace("(\.\d+)$","").duplicated()]
dataset.iloc[:,-1] = dataset.iloc[:,-1].astype('category')

dataset.replace({'Infinity': '0', np.nan:'0'}, inplace=True)

goldeneye =  pd.DataFrame()
hulk = pd.DataFrame()
benign = pd.DataFrame()
heartbleed = pd.DataFrame()

goldeneye = dataset[dataset['Label']=='DoS GoldenEye']
benign = dataset[dataset['Label']=='BENIGN']
hulk = dataset[dataset['Label']=='DoS Hulk']
heartbleed = dataset[dataset['Label']=='Heartbleed']

goldeneye.to_csv('GoldenEye.csv', index = False, sep=',')
benign.to_csv('Benign.csv', index = False, sep=',')
hulk.to_csv('Hulk.csv', index = False, sep=',')
heartbleed.to_csv('Heartbleed.csv', index = False, sep=',')