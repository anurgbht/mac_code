import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split

############################################################################################################
############################################################################################################
############################################################################################################

def my_predict_proba(clf, X):
    
    n_classes = clf.n_classes_
    
    if clf.algorithm == 'SAMME.R':
        # The weights are all 1. for SAMME.R
        proba = sum(samme_proba(estimator, n_classes, X)
                    for estimator in clf.estimators_)
        
    else:   # self.algorithm == "SAMME"
        proba = sum(estimator.predict_proba(X) * w
                    for estimator, w in zip(clf.estimators_,
                                            clf.estimator_weights_))

    proba /= clf.estimator_weights_.sum()
    proba = np.exp((1. / (n_classes - 1)) * proba)
    normalizer = proba.sum(axis=1)[:, np.newaxis]
    normalizer[normalizer == 0.0] = 1.0
    proba /= normalizer

    return [x[-1] for x in proba]
		
		
def samme_proba(estimator, n_classes, X):

    proba = estimator.predict_proba(X)
    proba[proba < np.finfo(proba.dtype).eps] = np.finfo(proba.dtype).eps
    log_proba = np.log(proba)

    return (n_classes - 1) * (log_proba - (1. / n_classes)
                              * log_proba.sum(axis=1)[:, np.newaxis])

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = AdaBoostClassifier(algorithm = 'SAMME.R',n_estimators = 2000)
clf.fit(X_train,y_train)

print(confusion_matrix(y_test,clf.predict(X_test)))

plt.plot(my_predict_proba(clf,X),[x[-1] for x in clf.predict_proba(X)],'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()
