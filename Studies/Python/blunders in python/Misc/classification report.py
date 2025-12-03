import os
import numpy as np
import pylab as plt
import pandas as pd
from sklearn import metrics
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

###############################################################################################################
###############################################################################################################
###############################################################################################################

def make_data():
    # sample data for a classification problem
    dat = load_breast_cancer()
    print(dat.data.shape)

    X = dat.data
    ##X.columns = boston.feature_names
    y = dat.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    clf = LogisticRegression()
    clf.fit(X_train,y_train)

    train_pred = pd.DataFrame(clf.predict_proba(X_train)).iloc[:,-1]

    return train_pred,list(y_train)


def plot_roc(y_true, y_score, buffer=0.005):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_score, drop_intermediate=False)
    roc_auc = metrics.auc(fpr, tpr)

    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, color='b', label = 'AUC = %0.4f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0-buffer, 1])
    plt.ylim([0, 1+buffer])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

def roc_curve_excel(y_true, y_score, decile=10):

    roc_data = pd.DataFrame(list(zip(y_true,y_score)), columns=['y_true','y_score'])
    
    roc_data['threshold'] = pd.qcut(roc_data['y_score'], decile)
    roc_data['decile'] = pd.qcut(roc_data['y_score'], decile, labels=False)              
    #return roc_data
    return roc_data.pivot_table(index=decile, columns='y_true', aggfunc='count')


###############################################################################################################
###############################################################################################################
###############################################################################################################

global thresh
thresh = 0.5

pred_proba,actual = make_data()
pred = [1 if x > thresh else 0 for x in pred_proba]

# Create a Pandas dataframe from the data.
df = pd.concat([pd.Series(actual),pred_proba],axis=1)
df.columns = ['y_actual','p']

# Create a Pandas Excel writer using XlsxWriter as the engine.

writer     = pd.ExcelWriter('classification_report.xlsx', engine='xlsxwriter')
df = df.sort_values(by='p',axis=0).reset_index().drop('index',1)
df.to_excel(writer, sheet_name="Raw Data")

metric = {'EM' : ["Accuracy","AUC","Gini","KS_value","Kappa","No Information Rate","Sensitivity","Specificity","Pos Pred Value","Neg Pred Value","F1","Prevalence","KS_decile","Total Records"],
          'MV' : [0.01 for x in range(14)]}

metric['MV'][metric['EM'].index('Accuracy')] = metrics.accuracy_score(actual,pred)
metric['MV'][metric['EM'].index('F1')] = metrics.f1_score(actual,pred)

conf_metr = pd.DataFrame(metrics.confusion_matrix(actual,pred))
conf_metr.index = ['actual 0','actual 1']
conf_metr.columns = ['predicted 0','predicted 1']

metric = pd.DataFrame(metric)
metric.to_excel(writer,sheet_name = "Report",index=False)
conf_metr.to_excel(writer,sheet_name = "Report",startrow = 20,startcol=0)

plot_roc(actual, pred_proba)


writer.save()
