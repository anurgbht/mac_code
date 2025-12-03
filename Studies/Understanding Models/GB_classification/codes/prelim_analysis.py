import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

############################################################################################################
############################################################################################################
############################################################################################################

def my_predict(clf,X):
    tt = clf.init_.predict(X)
    for est in clf.estimators_:
        tt = [y + clf.get_params()['learning_rate']*x for x,y in zip(est[0].predict(X),tt)]
    tt = [np.exp(x)/(1+np.exp(x)) for x in tt]
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

clf = GradientBoostingClassifier()
clf.fit(X_train,y_train)

print(confusion_matrix(y_test,clf.predict(X_test)))

plt.plot(my_predict(clf,X),[x[-1] for x in clf.predict_proba(X)],'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()
