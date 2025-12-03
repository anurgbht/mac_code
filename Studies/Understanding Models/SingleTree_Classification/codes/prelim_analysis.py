import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn import tree
from sklearn.metrics import *
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

############################################################################################################
############################################################################################################
############################################################################################################

def my_predict(clf,X):
    print(X.shape)
    tt = np.zeros(X.shape[0])
    for est in clf.estimators_:
        tt = [y + x for x,y in zip([pp[-1] for pp in est.predict_proba(X)],tt)]
    tt = [x/clf.get_params()['n_estimators'] for x in tt]
    return tt



############################################################################################################
############################################################################################################
############################################################################################################

dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = tree.DecisionTreeClassifier()
clf.fit(X_train,y_train)

joblib.dump(clf,"my_clf.pkl")
