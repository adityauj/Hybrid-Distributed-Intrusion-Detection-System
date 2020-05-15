from sklearn.ensemble import VotingClassifier
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection  import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import time

if __name__ == '__main__':
    dataset = pd.read_csv("reduced.csv",low_memory=True,skipinitialspace=True)
    
    X = dataset.drop('Label', axis=1)
    y = dataset['Label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)  
    
    dtc = DecisionTreeClassifier()  
    knnc = KNeighborsClassifier(n_neighbors=3, n_jobs = -1)  
    
    start = time.time()
    eclf1 = VotingClassifier(estimators=[('dt', dtc), ('knn', knnc)], voting='hard', n_jobs=-1)
    eclf1 = eclf1.fit(X_train, y_train)
    print(time.time() - start)
    y_pred = eclf1.predict(X_test)  
    
    print(confusion_matrix(y_test, y_pred))  
    print(accuracy_score(y_test, y_pred))  
    print(classification_report(y_test, y_pred))
