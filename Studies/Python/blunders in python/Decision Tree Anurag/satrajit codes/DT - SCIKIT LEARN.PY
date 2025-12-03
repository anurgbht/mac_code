
##python -m pip install matplotlib (run the code on the left to install matplotlib from cmd D:)
##python -m pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org pydot

import pandas as pandas
import pydotplus as pydot
import datetime
import math
import os
from sklearn import tree
import graphviz
from subprocess import check_call


pandas.set_option('display.max_rows', 8000)
pandas.set_option('display.precision', 2)

start_time = datetime.datetime.now()
print(("Start Date & Time: %s-%s-%s %s:%s:%s")%(start_time.day, start_time.month, start_time.year, start_time.hour, start_time.minute, start_time.second)) 

os.chdir("D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/SatrajitKar/TataSteel/Python_WS/tuyer_data/DT_validation/")
FeatureDat_DT = pandas.read_csv("FeatureDat_DT_V3.csv", header=0, sep=',', parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
df2 = FeatureDat_DT.fillna(-99999)
 
X = df2.values[:,0:523]
Y = df2.values[:,523]

clf = tree.DecisionTreeClassifier(criterion='gini', random_state=42, max_depth = 7, min_samples_leaf = 20, class_weight={0:10,1:1})
clf = clf.fit(X,Y)
dot_data = tree.export_graphviz(clf, out_file='tree.dot')


