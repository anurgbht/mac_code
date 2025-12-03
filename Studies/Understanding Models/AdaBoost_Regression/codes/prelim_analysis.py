import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn import tree
from sklearn.metrics import *
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor

############################################################################################################
############################################################################################################
############################################################################################################

def _get_median_predict(clf, X, limit):
    # Evaluate predictions of all estimators
    predictions = np.array([
        est.predict(X) for est in clf.estimators_[:limit]]).T

    # Sort the predictions
    sorted_idx = np.argsort(predictions, axis=1)

    # Find index of median prediction for each sample
    weight_cdf = np.cumsum(clf.estimator_weights_[sorted_idx], axis=1)
    median_or_above = weight_cdf >= 0.5 * weight_cdf[:, -1][:, np.newaxis]
    median_idx = median_or_above.argmax(axis=1)

    median_estimators = sorted_idx[np.arange(X.shape[0]), median_idx]

    # Return median predictions
    return predictions[np.arange(X.shape[0]), median_estimators]

def my_predict(clf, X):
    return _get_median_predict(clf,X, len(clf.estimators_))

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_boston()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = AdaBoostRegressor( n_estimators=5)
clf.fit(X_train,y_train)

plt.plot(my_predict(clf,X),clf.predict(X),'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()


X = X[:2]

limit = len(clf.estimators_)

# Evaluate predictions of all estimators
predictions = np.array([
    est.predict(X) for est in clf.estimators_[:limit]]).T

# Sort the predictions
sorted_idx = np.argsort(predictions, axis=1)

# Find index of median prediction for each sample
weight_cdf = np.cumsum(clf.estimator_weights_[sorted_idx], axis=1)
median_or_above = weight_cdf >= 0.5 * weight_cdf[:, -1][:, np.newaxis]
median_idx = median_or_above.argmax(axis=1)

median_estimators = sorted_idx[np.arange(X.shape[0]), median_idx]

# Return median predictions
my_pred = predictions[np.arange(X.shape[0]), median_estimators]
