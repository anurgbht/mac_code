import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics.pairwise import rbf_kernel,polynomial_kernel

############################################################################################################
############################################################################################################
############################################################################################################

def my_predict(clf,X_test):
    y_alpha = clf.dual_coef_[0]
    tt = polynomial_kernel(clf.support_vectors_,X_test,clf.degree,1./X_test.shape[1],clf.coef0)*y_alpha[:,np.newaxis]
    tt = tt.sum(axis=0)+clf.intercept_
    return tt

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_boston()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = SVR(kernel='poly',degree=2)
clf.fit(X_train,y_train)

plt.plot(my_predict(clf,X),clf.predict(X),'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()
