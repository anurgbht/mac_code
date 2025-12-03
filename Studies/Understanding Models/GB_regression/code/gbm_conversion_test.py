import os
import Lime_all_trees as lime
import Ore_all_trees as ore
import Oxygen_all_trees as oxy
import numpy as np
from sklearn.externals import joblib

################################################################################
################################################################################
################################################################################

def my_gbm_predict(clf,X):
    X = np.array(X).reshape(1,-1)
    pred = [0 for i in range(len(X))]
    for est in clf.estimators_:
        est = est[0]
        pred = [x + y for x,y in zip(est.predict(X),pred)]
    return pred
        
def my_gbm_predict_raw(X):
    pred = []
    for x in X:
        pred.append(my_gbm_predict_raw_single(x))
    return pred

def my_gbm_predict_raw_single(X):
    pred = 0
    for est in lime.all_pred_func:
        pred += est(X)
    pred = lime.ybar + lime.lam*pred
    return pred



################################################################################
################################################################################
################################################################################

x = [[0,1,-22,1,0,-2]]
clf = joblib.load('lime_GBR.pkl')

print(clf.predict(np.array(x).reshape(1,-1)))
print(my_gbm_predict_raw(x))
