import os
import numpy as np
import pylab as plt
import pandas as pd
import itertools
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import confusion_matrix

############################################################################################################
############################################################################################################
############################################################################################################

def give_range(y,tt1=None,tt2=None):
    if not tt1:
        print('Changing the buckets')
        tt1 = [min(y),np.percentile(y,10),np.percentile(y,25),np.percentile(y,50),np.percentile(y,75),np.percentile(y,90)]
        tt2 = [np.percentile(y,10),np.percentile(y,25),np.percentile(y,50),np.percentile(y,75),np.percentile(y,90),max(y)]

    y_cat = []
    for i in y:
        count = 0
        for j in range(len(tt1)):
            if ((i<=tt2[j]) and (i>tt1[j])):
                y_cat.append(j)
                count += 1
        if count == 0:
            y_cat.append(len(tt1))
            
    return y_cat,tt1,tt2
                
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure()
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
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

clf = RandomForestRegressor()
clf.fit(X_train,y_train)

y_cat,tt1,tt2 = give_range(y)

y_cat_train,tt1,tt2 = give_range(y_train,tt1,tt2)
y_cat_test,tt1,tt2 = give_range(y_test,tt1,tt2)

y_cat_train_pred,tt1,tt2 = give_range(clf.predict(X_train),tt1,tt2)
y_cat_test_pred,tt1,tt2 = give_range(clf.predict(X_test),tt1,tt2)
y_cat_all_pred,tt1,tt2 = give_range(clf.predict(X),tt1,tt2)

plot_confusion_matrix(confusion_matrix(y_cat_test,y_cat_test_pred),classes=tt1+[tt2[-1]])
