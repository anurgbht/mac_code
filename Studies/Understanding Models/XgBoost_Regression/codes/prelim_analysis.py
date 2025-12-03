import os
import re
import numpy as np
import pylab as plt
import pandas as pd
from sklearn.metrics import *
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from xgboost.sklearn import XGBRegressor
from sklearn.externals import joblib

############################################################################################################
############################################################################################################
############################################################################################################
def make_text(leaf_node,leaf_descr,node_descr,parent_child,child_parent,fw):
    value = leaf_descr[leaf_node]
    c = leaf_node
    flag = 1
    condition = "\n\tif ( "
    while flag == 1:
        try:
            p = child_parent[c]
            if parent_child[p].index(c) == 1:
                condition += "(" + node_descr[p].split("<")[0] + " >= " + node_descr[p].split("<")[1] + ") and "
            else:
                condition += "(" + node_descr[p] + ") and "
            c = p
        except:
            flag = 0
    condition = condition[:-4] + ") : \n\t\t" + "pred = " + str(leaf_descr[leaf_node])
    fw.write(condition)

def make_beginning(fw,dot_file_name):
    tt = "\ndef " + dot_file_name.split('.')[0] + "(X) :"
    fw.write(tt)

def make_end(fw):
    tt = "\n\treturn pred\n\n"
    fw.write(tt)

def make_code():
    separate_booster()
    write_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Employee Personal/practice/Understanding Models/XgBoost_Regression/codes/"
    os.chdir("D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Employee Personal/practice/Understanding Models/XgBoost_Regression/data/")
    fw = open(write_path+"T_all_trees.py","w")
    all_pred_func = "\n\nall_pred_func = ["
    
    for booster in os.listdir():
        parent = []
        child = []
        leaves = []
        node_descr = {}
        leaf_descr = {}
        parent_child = {}
        child_parent = {}
        f = open(booster,"r")
        for line in f:
            if 'yes' in line:
                tt = re.findall(r'\d+',line)
                parent.append(tt[0])
                child.append(tt[4])
                child.append(tt[5])
                node_descr[tt[0]] = "X[{0}] < {1}.{2}".format(tt[1],tt[2],tt[3])
                parent_child[tt[0]] = [tt[4],tt[5]]
                child_parent[tt[4]] = tt[0]
                child_parent[tt[5]] = tt[0]
            elif 'leaf' in line:
                leaf_descr[re.findall(r'\d+',line)[0]] = re.findall(r'=.+',line)[0][1:]
                leaves.append(re.findall(r'\d+',line)[0])
        
        make_beginning(fw,booster)
        for leaf in leaves:
            make_text(leaf,leaf_descr,node_descr,parent_child,child_parent,fw)
        make_end(fw)
        all_pred_func +=  booster.split('.')[0] + ','
        

    all_pred_func = all_pred_func[:-1]
    all_pred_func += "]\n"
    fw.write(all_pred_func)
    fw.close()

def separate_booster():
    write_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Employee Personal/practice/Understanding Models/XgBoost_Regression/data/"
    for file in os.listdir(write_path):
        os.remove(write_path+file)
    count = -1
    f = open("dump.txt","r")
    for line  in f.readlines():
        if "booster" in line:
            count += 1
            f_temp = open(write_path+"dump_"+str(count).zfill(4)+".txt","w")
        else:
            f_temp = open(write_path+"dump_"+str(count).zfill(4)+".txt","a+")
        
        f_temp.write(line.replace('\t',''))
        f_temp.close()

def my_predict(X):
    tt = []
    for i in X:
        temp_pred = 0
        for est in at.all_pred_func:
            temp_pred += est(i)
        tt.append(temp_pred)
    return tt

############################################################################################################
############################################################################################################
############################################################################################################

dat = load_boston()
print(dat.data.shape)

X = dat.data
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

##clf = XGBRegressor(n_estimators=150)
##clf.fit(X_train,y_train)
##joblib.dump(clf,"my_xgboost.pkl")
##clf.get_booster().dump_model("dump.txt")
##make_code()

import T_all_trees as at
clf = joblib.load('my_xgboost.pkl')
plt.plot(my_predict(X),clf.predict(X),'.')
plt.xlabel("my prediction")
plt.ylabel("sklearn prediction")
plt.minorticks_on()
plt.grid(1,which='both')
plt.show()
