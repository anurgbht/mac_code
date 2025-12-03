import os
import pandas as pd
import numpy as np
import regression_module as regr
import classification_module as cls
from sklearn.datasets import load_boston
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pylab as plt


############################################################################################################
############################################################################################################
############################################################################################################

#### Regression example
##
##dat = load_boston()
##print(dat.data.shape)
##
##X = dat.data
####X.columns = boston.feature_names
##y = dat.target
##
##X_train, X_test, y_train, y_test = train_test_split(X,y)
##
####regr.prelim_keras(X_train, X_test, y_train, y_test)
##
#### check the listing of available models at regr.print_available_models
##regr.print_available_models()
##
#### a subset of the models can be chosen by indexing the list accordingly
##model_list = regr.available_models
##all_models = regr.make_multiple(X_train, X_test, y_train, y_test,model_list)

############################################################################################################
############################################################################################################
############################################################################################################

## Classification example

dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X,y)
cls.print_available_models()

clf = cls.prelim_logit(X_train, X_test, y_train, y_test)

model_list = cls.available_models
all_models = cls.make_multiple(X_train, X_test, y_train, y_test,model_list)
