import os
import numpy as np
import pandas as pd
import random
import pylab as plt
from datetime import datetime

##################################################################################################
##################################################################################################

def question_1():
    test_1 = pd.read_csv('sample_csv.csv')

    print(min(test_1.iloc[:,2]))
    print(min(test_1.loc[:,'C.speed']))

    tt = []

    for col in test_1:
        temp = test_1.loc[:,col]
        q = [min(temp),max(temp),np.average(temp)]
        q.extend([np.percentile(temp,(x+1)/10) for x in range(9)])
        tt.append(q)
    pd.DataFrame(tt).to_csv('output_1.csv')

    # plotting part of the assignment

    plt.subplot(2,1,1)
    x = test_1.loc[:,'TimeStamp']
    y1 = test_1.loc[:,'TC7']
    y2 = test_1.loc[:,'TC27']
    y3 = test_1.loc[:,'TC47']
    y4 = test_1.loc[:,'TC67']
    plt.plot(x,y1,x,y2,x,y3,x,y4)
    plt.grid(1)
    plt.ylabel('Temperature')
    plt.legend(['layer 1','layer 2','layer 3','layer 4'])

    plt.subplot(2,1,2)
    y = y1 = test_1.loc[:,'C.speed']
    plt.plot(x,y)
    plt.grid(1)
    plt.ylabel('Casting Speed')
    plt.xlabel('Time')
    plt.legend(['Casting Speed'])

    plt.suptitle('Python Assessment Plot')
    plt.show()

##################################################################################################

def question_2():
    test_21 = pd.read_excel('sample_excel.xlsx',sheetname='DateTime Data')

    test_21.loc[:,'Deliv Date'] = [datetime.strptime(x,'%d.%m.%Y') for x in test_21.loc[:,'Deliv Date']]

    all_filter1 = [((x.month == 1)&(x.year == 2017)) for x in test_21.loc[:,'Deliv Date']]
    temp1 = test_21.loc[all_filter1,'Order Qty']
    print(np.average(temp1))

    all_filter2 = [((x.month == 3)&(x.year == 2016)) for x in test_21.loc[:,'Deliv Date']]
    temp2 = test_21.loc[all_filter2,'Timely Delivery Qty']
    print(sum(temp2.isnull()))

    all_filter3 = [(x.year == 2016) for x in test_21.loc[:,'Deliv Date']]
    temp3 = test_21.loc[all_filter3,'Order Qty']
    plt.hist(temp3,bins = 25)
    plt.grid()
    plt.title('max : ' + str(max(temp3)) + ' mean : ' + str(np.average(temp3)))
    plt.show()
        

##################################################################################################
##################################################################################################

os.chdir('D:/Confidential/LnD/python evaluation/')

##question_1()
##question_2()

test_22 = pd.read_excel('sample_excel.xlsx',sheetname='Null Data')
print(test_22.loc[:,'Vendor'].value_counts())
tt = []
for v_id in test_22.loc[:,'Vendor'].unique():
    tt2 = [v_id]
    for m_id in test_22.columns.drop('Vendor'):
        temp = test_22.loc[test_22.loc[:,'Vendor'] == v_id,m_id]
        tt2.extend([sum(temp.isnull())])
    tt.append(tt2)

print(tt)
