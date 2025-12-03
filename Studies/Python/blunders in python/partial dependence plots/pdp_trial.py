import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
from sklearn.linear_model import LinearRegression

############################################################################################################
############################################################################################################
############################################################################################################

def make_dat(x_avg,i,tt):
    ret_tt = []
    tt_temp = []
    for j in tt:
        ret_tt.append(x_avg)
    ret_tt = pd.DataFrame(ret_tt)
    ret_tt.iloc[:,i] = tt
    return ret_tt

def pdp_vis(clf,X,names):
    x_avg = list(X.mean(axis=0))
    x_min = X.min(axis=0)
    x_max = X.max(axis=0)
    nx = len(x_avg)
    ns = 10000

    for i in range(nx):
        tt = np.linspace(x_min[i],x_max[i],ns)
        X_temp = make_dat(x_avg,i,tt)
        X_temp.to_csv('temp.csv')
        pred = clf.predict(X_temp)
        plt.plot(tt,pred)
        plt.title(names[i])
        plt.ylabel('Predicted')
        plt.xlabel(names[i])
        plt.grid(1)
        plt.show()
        
############################################################################################################
############################################################################################################
############################################################################################################

dat = load_boston()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = RandomForestRegressor(n_estimators = 1000)
clf.fit(X_train,y_train)

pdp_vis(clf,X,dat.feature_names)
