
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def trial3():
	person_id = input('please enter the person you want the data for : ')
	#path = 'D:/Bhatt/2016-08/Hypothesis testing training/data/'+str(person_id)+'.csv'
	path = os.getcwd()+'\\data\\'+str(person_id)+'.csv'
	temp = pd.read_csv(path)
	temp.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	act_id = [1,3,4,5,7]
	for i in range(0,5):
		x_temp = temp.x_acc[temp.action_flag == act_id[i]]+1000
		y_temp = temp.y_acc[temp.action_flag == act_id[i]]+500
		z_temp = temp.z_acc[temp.action_flag == act_id[i]]
		ind_temp = temp.index[temp.action_flag == act_id[i]]/3120.0
		plt.subplot(2,3,i+1)
		plt.plot(ind_temp,x_temp,'r',ind_temp,y_temp,'g',ind_temp,z_temp,'b');
	
	plt.show()

trial3()
