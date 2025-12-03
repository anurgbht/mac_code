## General imports
import os
import pylab as plt
import numpy as np

## sklearn imports
from sklearn.svm import SVC
from sklearn.metrics import *
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

## keras imports
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout

## XGBoost imports
from xgboost import XGBClassifier

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

global plot_flag
plot_flag = 0

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def prelim_keras(X_train,X_test,y_train,y_test):
    print('Preliminary Keras-Classification Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    input_dim = X_train.shape[1]
    
    clf = Sequential()
    clf.add(Dense(input_dim, input_dim=input_dim, activation='sigmoid'))
    clf.add(Dropout(0.3))
    clf.add(Dense(input_dim, activation='sigmoid'))
    clf.add(Dropout(0.3))
    clf.add(Dense(1, activation='sigmoid'))
    # Compile clf
    clf.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the clf
    clf.fit(X_train, y_train,epochs=150, batch_size=int(X_train.shape[0]/10),  verbose=0)

    pred_test = [1 if x[0] > 0.5 else 0 for x in clf.predict(X_test)]
    pred_train = [1 if x[0] > 0.5 else 0 for x in clf.predict(X_train)]
    
    print("Confusion matrix for Preliminary Keras-Classification Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))

    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary Keras-ANN Analysis")
    
    return clf

def prelim_knn(X_train,X_test,y_train,y_test):
    print('Preliminary KNN Analysis')

    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary KNN Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))
    
    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary kNN Analysis")
    
    return clf


def prelim_GBM(X_train,X_test,y_train,y_test):
    print('Preliminary GBM Analysis')

    clf = GradientBoostingClassifier()
    clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary GBM Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))
    
    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary GBM Analysis")

    return clf

def single_tree(X_train,X_test,y_train,y_test):
    print('Preliminary single tree analysis')

    clf = tree.DecisionTreeClassifier(min_samples_leaf=25)
    clf = clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary Single Tree Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))
    
    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary Single Tree Analysis")
    
    return clf

def prelim_RF(X_train,X_test,y_train,y_test):
    print('Preliminary Random Forest Analysis')

    clf = RandomForestClassifier(max_depth=5)
    clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary RF Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))
    
    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary Random Forest Analysis")

    return clf

def prelim_logit(X_train,X_test,y_train,y_test):
    print('Preliminary Logistic Analysis')

    clf = LogisticRegression()
    clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary Logistic Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))

    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary Logistic Analysis")
    
    return clf

def prelim_svm(X_train,X_test,y_train,y_test):
    print('Preliminary SVM Analysis')

    clf = SVC(probability=True,kernel='rbf', C=.1,gamma=1)
    clf.fit(X_train,y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)

    print("Confusion matrix for Preliminary SVM Analysis")
    print("Train confusion matrix")
    print(confusion_matrix(y_train,pred_train))
    print("Teest confusion matrix")
    print(confusion_matrix(y_test,pred_test))
    
    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary SVM Analysis")

    return clf
    
def prelim_XGBC(X_train,X_test,y_train,y_test):
    print('Preliminary X - Gradient Boosting Classification Analysis')

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    clf = XGBClassifier()
    # Fit the clf
    clf.fit(X_train, y_train)

    # calculate predictions
    X_test = np.array(X_test)
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)

    my_plot(X_train,X_test,y_train,y_test,clf,"Preliminary XGBoost Analysis")

    return clf


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def my_plot(X_train,X_test,y_train,y_test,clf,sup_title):

    print("Plot flag is : ",plot_flag)
    if 'Keras' in sup_title:
        prob_train = np.array([x[0] for x in clf.predict(X_train)])
        prob_test = np.array([x[0] for x in clf.predict(X_test)])
    else:    
        prob_train = np.array([x[-1] for x in clf.predict_proba(X_train)])
        prob_test = np.array([x[-1] for x in clf.predict_proba(X_test)])
    
    bins = np.linspace(0,1.1,25)

    if plot_flag == 1:
        plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
    
    plt.subplot(122)
    plt.title('Test')
    plt.hist([prob_test[y_test==1],prob_test[y_test==0]],bins,label = ['y = 1','y = 0'])
    plt.legend()
    plt.grid(1)

    plt.subplot(121)
    plt.title('Train')
    plt.hist([prob_train[y_train==1],prob_train[y_train==0]],bins,label = ['y = 1','y = 0'])
    plt.legend()
    plt.grid(1)
    plt.suptitle(sup_title)
    
    # try without an except is not permitted
    try:
        os.mkdir(os.getcwd() + "\\plots_classification\\")
    except:
        print("Folder already exists.")
        
    if plot_flag == 1:
        plt.savefig(os.getcwd() + "\\plots_classification\\" + sup_title+'.png')
        plt.close()
    else:
        plt.show()



def print_available_models():
    for mod in available_models:
        print(mod.__name__)

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def make_multiple(X_train,X_test,y_train,y_test,model_list):
    tt = []
    global plot_flag
    plot_flag = 1
    for func_name in model_list:
        tt.append(func_name(X_train,X_test,y_train,y_test))

    return tt

available_models = [prelim_RF, prelim_GBM, prelim_keras, prelim_knn, prelim_logit, prelim_svm, single_tree, prelim_XGBC]
