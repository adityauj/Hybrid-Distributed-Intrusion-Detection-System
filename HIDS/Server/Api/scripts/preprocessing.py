def run():

	from sklearn.externals import joblib
	from sklearn.ensemble import ExtraTreesClassifier
	import csv
	import numpy as np
	import pandas as pd

	np.seterr(divide='ignore', invalid='ignore')

	dataset = pd.read_csv("dataset.csv", low_memory=False,skipinitialspace=True)
	dataset = dataset.loc[:,~dataset.columns.str.replace("(\.\d+)$","").duplicated()]
	dataset.iloc[:,-1] = dataset.iloc[:,-1].astype('category')

	dataset.replace({'Infinity': '0', np.nan:'0'}, inplace=True)

	dataset['Flow Byts/s'] = dataset['Flow Byts/s'].str.replace('','').astype(np.float64)
	dataset['Flow Pkts/s'] = dataset['Flow Pkts/s'].str.replace('','').astype(np.float64)

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
	