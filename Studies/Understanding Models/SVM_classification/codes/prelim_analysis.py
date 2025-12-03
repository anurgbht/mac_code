import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics.pairwise import rbf_kernel

############################################################################################################
############################################################################################################
############################################################################################################

def my_kernel(clf,X_train,xi):
    y_alpha = clf.dual_coef_[0]
    gamma = 1./X_train.shape[1]
    tt = y_alpha*rbf_kernel(X_train,xi,gamma)
    return tt

def my_predict(clf,X_test):
    y_alpha = clf.dual_coef_[0]
    tt = rbf_kernel(clf.support_vectors_,X_test)*y_alpha[:,np.newaxis]
    tt = tt.sum(axis=0)+clf.intercept_
    tt2 = [1 if x>=0 else 0 for x in tt]
    return tt2,tt

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data.T[:4].T
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = SVC()
clf.fit(X_train,y_train)

tt1,tt2 = my_predict(clf,X)

print(confusion_matrix(tt1,clf.predict(X)))
plt.plot(tt2,clf.decision_function(X),'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()


'''
############################################################################################################
############################################################################################################
############################################################################################################

def my_predict(clf,X):
    tt = []
    for i in X:
        tt.append(np.sign(np.inner(i,clf.coef_)+clf.intercept_))
    tt = [0 if x < 0 else 1 for x in tt]
    return tt

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data.T[:4].T
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = LinearSVC()
clf.fit(X_train,y_train)

print(confusion_matrix(my_predict(clf,X_test),clf.predict(X_test)))

plt.plot(my_predict(clf,X),clf.predict(X),'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()
'''
