import pandas as pd
import regression_module as regr
import classification_module as cls
from sklearn.datasets import load_boston
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

############################################################################################################
############################################################################################################
############################################################################################################

## Regression example

##dat = load_boston()
##print(dat.data.shape)
##
##X = dat.data
####X.columns = boston.feature_names
##y = dat.target

dat = pd.read_csv('train.csv')
X_train = dat.iloc[:,:-1]
y_train = dat.iloc[:,-1]

dat = pd.read_csv('test.csv')
X_test = dat.iloc[:,:-2]
y_test = dat.iloc[:,-2]
y_buffer = dat.iloc[:,-1]

##X_train, X_test, y_train, y_test = train_test_split(X,y)

## one-off example
#regr.prelim_keras(X_train, X_test, y_train, y_test)

## check the listing of available models at regr.print_available_models
regr.print_available_models()

## calling a function to run all the available models
## a subset of the models can be chosen by indexing the list accordingly
model_list = regr.available_models
all_models = regr.make_multiple(X_train, X_test, y_train, y_test,model_list)

############################################################################################################
############################################################################################################
############################################################################################################

###### Classification example
####
##dat = load_breast_cancer()
##print(dat.data.shape)
##
##X = dat.data
####X.columns = boston.feature_names
##y = dat.target
##
##X_train, X_test, y_train, y_test = train_test_split(X,y)
##cls.print_available_models()
##
#### one-off example
##clf = cls.prelim_logit(X_train, X_test, y_train, y_test)
##
#### calling a function to run all the available models
#### a subset of the models can be chosen by indexing the list accordingly
##model_list = cls.available_models
##all_models = cls.make_multiple(X_train, X_test, y_train, y_test,model_list)
