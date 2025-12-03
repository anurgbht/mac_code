
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
def trial4():
	person_id = input('please enter the person you want the data for : ')
	path = os.getcwd()+'\\data\\'+str(person_id)+'.csv'
	temp = pd.read_csv(path)
	temp.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	for i in range(1,8):
		x_temp = temp.x_acc[temp.action_flag == i]+1000
		y_temp = temp.y_acc[temp.action_flag == i]+500
		z_temp = temp.z_acc[temp.action_flag == i]
		#norm_temp = np.sqrt(np.square(x_temp)+np.square(y_temp)+np.square(z_temp))
		ind_temp = temp.index[temp.action_flag == i]/3120.0
		plt.subplot(3,3,i)
		#plt.plot(ind_temp,x_temp,'r',ind_temp,y_temp,'g',ind_temp,z_temp,'b',ind_temp,norm_temp,'k');
		plt.plot(ind_temp,x_temp,'r',ind_temp,y_temp,'g',ind_temp,z_temp,'b');
		
	plt.show()

trial4()
