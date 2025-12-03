import pandas as pd
import wfdb
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
from matplotlib  import cm
from collections import Counter
import scipy
import pickle
from scipy import signal

def rms_calc(a):
    rms = np.sqrt(np.mean(np.square(a)))
    return(rms)

def meanval_gen(p):
    from numpy.polynomial.hermite import hermfit
    print('Generating feature vectors for : ',p)
    sig, fields = wfdb.rdsamp(p)
    annsamp, anntype, subtype, chan, num, aux, annfs = wfdb.rdann(p, 'atr')
    meanval=[]
    for i in range(3,len(anntype)-3):
        temp_flag = anntype[i]
        if temp_flag not in ['+','|','~']:
            sig_temp,fields_temp = wfdb.rdsamp(p,sampfrom=annsamp[i]-50, sampto=annsamp[i]+50)
            df= pd.DataFrame(sig_temp)
            df.columns = ['a','b']
            pp=df['a']

            q1=pp.mean(0)
            pp=pp-q1
            
            b, a = signal.butter(3, 0.05)
            zi = signal.lfilter_zi(b, a)
            z, _ = signal.lfilter(b, a, pp, zi=zi*pp[0])
            z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
            pp = signal.filtfilt(b, a, pp)

            q2=pp.max()-pp.min()
            q3=rms_calc(pp)
            q4=scipy.stats.skew(pp)
            q5=scipy.stats.kurtosis(pp)
            q6=np.var(pp)
            q7=q5-3*(q6)**2
            tempx = np.linspace(-1,1,pp.size)
            tempq = hermfit(tempx, pp, 5)
            q8=tempq[0]
            q9=tempq[1]
            q10=tempq[2]
            q11=tempq[3]
            q12=tempq[4]
            q13=sum(np.absolute(np.fft.fft(pp)))
            meanval.append([q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,temp_flag])
    meanval = pd.DataFrame(meanval)
    return(meanval)

##meanval = meanval_gen('200')

##m1=meanval_gen('200')
##m2=meanval_gen('208')
##m3=meanval_gen('209')
##m4=meanval_gen('201')
##m5=meanval_gen('202')
##m6=meanval_gen('203')
##m7=meanval_gen('205')
##m8=meanval_gen('207')
##g1=meanval_gen('100')
##g2=meanval_gen('101')
##g3=meanval_gen('102')
##g4=meanval_gen('103')

##meanval=np.concatenate((m1,m2,m3,m4,m5,m6,m7,m8,g1,g2,g3,g4),axis=0)
##meanval=np.concatenate((m1,m2,m3,g1,g2),axis=0)
##meanval = pd.DataFrame(meanval)

##meanval.columns = ['amplitude','rms','skew','kurt','var','ekurt','h1','h2','h3','h4','h5','fft','label']

meanval = pickle.load( open( "meanval_store_filtered.pkl", "rb" ) )

print(Counter(meanval['label']).keys())
print(Counter(meanval['label']).values())

##label_list=['A','F','f','V','L','a','R','E','j']
label_list=['A']
temp_con = meanval['label'] == 'N'
for j in label_list:
    temp_con_temp = meanval['label'] == j
    temp_con = temp_con|temp_con_temp

meanval_all = meanval
meanval = meanval_all[temp_con]

temp=meanval['label']
temp2=list(set(temp))
temp3=[]
print(temp2)
for i in temp:
    temp3.append(temp2.index(i))

print(Counter(meanval['label']).keys())
print(Counter(meanval['label']).values())

fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(111)
ax.grid(True,linestyle='-',color='0.75')
t1=meanval['skew']
t2=meanval['h5']
ax.scatter(t1,t2,c=temp3, marker = 'o' );
plt.show()

## classifying the beats based on the feature vectors

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,accuracy_score
import random

portion_val=0.7
train_indices = random.sample(range(meanval.shape[0]),round(portion_val*(meanval.shape[0])))
test_indices = []
for i in range(0,meanval.shape[0]):
    if  i not in train_indices:
        test_indices.append(i)

x_train =  meanval.iloc[train_indices,0:-1]
y_train =  meanval.iloc[train_indices,-1]

x_test =  meanval.iloc[test_indices,0:-1]
y_test =  meanval.iloc[test_indices,-1]

clf = RandomForestClassifier(n_estimators=30)
clf = clf.fit(x_train, y_train)

guess = clf.predict(x_train)
print(confusion_matrix(guess,y_train))
print(accuracy_score(guess,y_train))

guess = clf.predict(x_test)
print(confusion_matrix(guess,y_test))
print(accuracy_score(guess,y_test))

importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(x_train.shape[1]):
    print("%d. %s (%f)" % (f + 1, x_train.columns[indices[f]], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(x_train.shape[1]), importances[indices], color="r", yerr=std[indices], align="center")
plt.xticks(range(x_train.shape[1]), indices)
plt.xlim([-1, x_train.shape[1]])
plt.show()

### K means clustering on the data
##
####from sklearn.cluster import KMeans
####from sklearn.metrics import silhouette_samples, silhouette_score
####
####nrange=[2,3,4,5,6,7,8,9]
####
####for nn in nrange:
####    kmeans = KMeans(n_clusters=nn).fit(x_train)
####    cluster_labels = kmeans.fit_predict(x_train)
####    silhouette_avg = silhouette_score(x_train, cluster_labels)
####    print(nn," : ",silhouette_avg)
##
## pickle code
pickle.dump(meanval_all,open('meanval_store_filtered.pkl',"wb"))
##
