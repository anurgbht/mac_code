## General imports
import os
import pylab as plt
import numpy as np

## sklearn imports
from sklearn.svm import SVR
from sklearn.metrics import *
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

## keras imports
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout

## XGBoost imports
from xgboost import XGBRegressor

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

global plot_flag
plot_flag = 1

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def prelim_keras(X_train,X_test,y_train,y_test):
    print('Preliminary Keras-ANN Analysis')

    input_dim  = X_train.shape[1]
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    #my_act = LeakyReLU(alpha=0.3)
    model = Sequential()
    model.add(Dense(2*input_dim, input_dim=input_dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(input_dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(input_dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1,kernel_initializer='normal'))
    # Compile clf
    model.compile(loss='mse', optimizer='adam')

    # Fit the clf
    history = model.fit(X_train, y_train,epochs=100, batch_size=int(X_train.shape[0]/10), verbose=0)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = model.predict(X_test)
    pred_test = [x[0] for x in pred_test]
    
    pred_train = model.predict(X_train)
    pred_train = [x[0] for x in pred_train]
    
    my_plot(pred_test,pred_train,y_test,y_train,'Keras Regression Analysis')

    return model

def prelim_linear(X_train,X_test,y_train,y_test):
    print('Preliminary OLS Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    clf = linear_model.LinearRegression()
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(pred_test,pred_train,y_test,y_train,'OLS Regression Analysis')

    return clf
    

def prelim_SVR(X_train,X_test,y_train,y_test):
    print('Preliminary Support Vector Regression Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # Fit the clf
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(pred_test,pred_train,y_test,y_train,'Support Vector Regression Analysis')

    return clf

def prelim_RFR(X_train,X_test,y_train,y_test):
    print('Preliminary Random Forest Regression Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    clf = RandomForestRegressor(n_estimators=20)
    # Fit the clf
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(pred_test,pred_train,y_test,y_train,'Random Forest Regression Analysis')

    return clf
    
def prelim_GBR(X_train,X_test,y_train,y_test):
    print('Preliminary Gradient Boosting Regression Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    clf = GradientBoostingRegressor()
    # Fit the clf
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(pred_test,pred_train,y_test,y_train,'Gradient Boosting Regression Analysis')

    return clf

def prelim_XGBR(X_train,X_test,y_train,y_test):
    print('Preliminary X - Gradient Boosting Regression Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    clf = XGBRegressor()
    # Fit the clf
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(pred_test,pred_train,y_test,y_train,'X-Gradient Boosting Regression Analysis')

    return clf

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################


def my_plot(pred_test,pred_train,y_test,y_train,sup_title):

    y_test = list(y_test)
    y_train = list(y_train)
    err_test = [x-y for x,y in zip(pred_test,y_test)]
    err_train = [x-y for x,y in zip(pred_train,y_train)]

    if plot_flag == 1:
        plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(2,2,1)
    plt.plot(pred_test,y_test,'.')
    plt.ylabel('Actual')
    plt.minorticks_on()
    plt.grid(1,'both')
    plt.title('Test RMS : {0:.3f}, R$^2$ = {1:.3f}'.format(np.sqrt(np.mean(np.square(err_test))),my_r2(pred_test,y_test)))

    plt.subplot(2,2,2)
    plt.plot(pred_train,y_train,'.')
    plt.minorticks_on()
    plt.grid(1,'both')
    plt.ylabel('Actual')
    plt.title('Train RMS : {0:.3f}, R$^2$ = {1:.3f}'.format(np.sqrt(np.mean(np.square(err_train))),my_r2(pred_train,y_train)))

    plt.subplot(2,2,3)
    plt.hist(err_test,bins = 150)
    plt.minorticks_on()
    plt.grid(1,'both')
    plt.title('Test : Mean error : {0:.3f}, Std of error : {1:.3f}'.format(np.average(err_test), np.std(err_test)))
    
    plt.subplot(2,2,4)
    plt.hist(err_train, bins = 150)
    plt.minorticks_on()
    plt.grid(1,'both')
    plt.title('Train : Mean error : {0:.3f}, Std of error : {1:.3f}'.format(np.average(err_train), np.std(err_train)))
	
    plt.suptitle(sup_title)

    # try without an except is not permitted
    try:
        os.mkdir(os.getcwd() + "\\plots_regression\\")
    except:
        print("Folder already exists.")
        
    if plot_flag == 1:
        plt.savefig(os.getcwd() + "\\plots_regression\\" + sup_title+'.png')
        plt.close()
    else:
        plt.show()

def my_r2(y_pred,y_act):
    sigma1 = np.sum([(x-y)**2 for x,y in zip(y_pred,y_act)])
    y_mean = np.average(y_act)
    sigma2 = np.sum([(x-y_mean)**2 for x in y_act])
    return 1-(sigma1/sigma2)

def print_available_models():
    for mod in available_models:
        print(mod.__name__)

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def make_multiple(X_train,X_test,y_train,y_test,model_list):
    tt = []
    plot_flag = 0
    for func_name in model_list:
        tt.append(func_name(X_train,X_test,y_train,y_test))

    return tt

available_models = [prelim_XGBR,prelim_GBR,prelim_RFR,prelim_SVR,prelim_linear,prelim_keras]
