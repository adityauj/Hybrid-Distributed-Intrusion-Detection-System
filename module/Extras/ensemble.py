from sklearn.ensemble import VotingClassifier
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import time

if __name__ == '__main__':

	dataset = pd.read_csv("reduced.csv",low_memory=False,skipinitialspace=True)

	X = dataset.drop('Label', axis=1)
	y = dataset['Label'] 

	dtc = DecisionTreeClassifier()  
	knnc = KNeighborsClassifier(n_neighbors=3, n_jobs=-1)  

	start = time.time()
	model = VotingClassifier(estimators=[('dt', dtc), ('knn', knnc)], voting='soft', n_jobs=-1)
	model = model.fit(X, y)
	print('Training time : ',time.time() - start)

	filename = 'ensemble.sav'
	joblib.dump(model, filename)
