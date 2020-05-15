import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection  import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.externals import joblib

dataset = pd.read_csv("reduced.csv",low_memory=True,skipinitialspace=True)

X = dataset.drop('Label', axis=1)
y = dataset['Label']

classifier = DecisionTreeClassifier(max_depth = 20)  
classifier.fit(X, y)  

filename = 'decisiontree.sav'

joblib.dump(classifier, filename)