import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection  import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.externals import joblib

from sklearn.ensemble import RandomForestClassifier



dataset = pd.read_csv("reduced.csv",low_memory=True,skipinitialspace=True)

X = dataset.drop('Label', axis=1)
y = dataset['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)  

clf = RandomForestClassifier()
clf.fit(X,y)

classifier = DecisionTreeClassifier(max_depth = 15)  
classifier.fit(X, y)  

y_pred = clf.predict(X_test)  

benign = pd.read_csv("benign.csv",low_memory=True,skipinitialspace=True)
testX = benign.drop('Label',axis =1) 
testy = benign['Label']

pred = clf.predict(testX)
dtpred = classifier.predict(testX)

print(confusion_matrix(y_test, y_pred))  
print(accuracy_score(y_test, y_pred))  
print(classification_report(y_test, y_pred))

filename = 'decisiontree.sav'

joblib.dump(classifier, filename)