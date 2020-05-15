from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.externals import joblib

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt


dataset = pd.read_csv("reduced.csv",low_memory=True,skipinitialspace=True)
dataset = dataset.drop("Label",axis = 1)

dataset = dataset.astype('float64')


clf = IsolationForest(n_jobs=-1, contamination =0.20)
clf.fit(dataset)

filename = 'isolationforest.sav'

joblib.dump(clf, filename)