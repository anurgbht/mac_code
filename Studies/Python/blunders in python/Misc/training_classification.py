import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

#########################################################################################################
#########################################################################################################
#########################################################################################################

# this loads the data
dat = load_breast_cancer()
print(dat.data.shape)

X = dat.data
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

## build the model on train and test data using the following methods
## 1. Logistic Regression
## 2. GBM
## 3. SVM (try out various kernels)
## 4. AdaBoost
## 5. XgBoost
## 6. Any other that you can think

## compare the model performances by multiple methods
## such as
## 1. accuracy
## 2. false positive rate
## 3. confusion matrix

