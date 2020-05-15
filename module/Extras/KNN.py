import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection  import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.externals import joblib

dataset = pd.read_csv("reduced.csv",low_memory=True,skipinitialspace=True)

X = dataset.drop('Label', axis=1)
y = dataset['Label']
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)  

classifier = KNeighborsClassifier(n_neighbors=3, n_jobs = -1)  
classifier.fit(X, y)

y_pred = classifier.predict(X_test)  

print(confusion_matrix(y_test, y_pred))  
print(accuracy_score(y_test, y_pred))  
print(classification_report(y_test, y_pred))

filename = 'knn.sav'
joblib.dump(classifier, filename)