
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def trail2():
	person_id = input('please enter the person you want the data for : ')
	activity_id = input('which activity ?? : ')
	#path = 'D:/Bhatt/2016-08/Hypothesis testing training/data/'+str(person_id)+'.csv'
	path = os.getcwd()+'\\data\\'+str(person_id)+'.csv'
	temp1 = pd.read_csv(path)
	temp1.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	x_temp = temp1.x_acc[temp1.action_flag == activity_id]+1000
	y_temp = temp1.y_acc[temp1.action_flag == activity_id]+500
	z_temp = temp1.z_acc[temp1.action_flag == activity_id]
	ind_temp = temp1.index[temp1.action_flag == activity_id]/3120.0
	plt.plot(ind_temp,x_temp,'r',ind_temp,y_temp,'g',ind_temp,z_temp,'b')
	plt.grid()
	plt.show()
	
trail2()
