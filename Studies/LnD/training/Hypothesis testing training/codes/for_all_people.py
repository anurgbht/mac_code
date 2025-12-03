
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trial1():
	activity_id = input('which activity ?? : ')
	temp1 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/1.csv')
	temp1.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp2 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/2.csv')
	temp2.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp3 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/3.csv')
	temp3.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp4 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/4.csv')
	temp4.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp5 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/5.csv')
	temp5.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp6 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/6.csv')
	temp6.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp7 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/7.csv')
	temp7.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp8 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/8.csv')
	temp8.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp9 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/9.csv')
	temp9.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp10 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/10.csv')
	temp10.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp11 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/11.csv')
	temp11.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp12 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/12.csv')
	temp12.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp13 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/13.csv')
	temp13.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp14 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/14.csv')
	temp14.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	temp15 = pd.read_csv('D:/Bhatt/2016-08/Hypothesis testing training/data/15.csv')
	temp15.columns = ['index','x_acc','y_acc','z_acc','action_flag']
	
	x_temp1 = temp1.x_acc[temp1.action_flag == activity_id]
	y_temp1 = temp1.y_acc[temp1.action_flag == activity_id]
	z_temp1 = temp1.z_acc[temp1.action_flag == activity_id]
	norm_temp1 = np.sqrt(np.square(x_temp1)+np.square(y_temp1)+np.square(z_temp1))
	
	x_temp2 = temp2.x_acc[temp2.action_flag == activity_id]
	y_temp2 = temp2.y_acc[temp2.action_flag == activity_id]
	z_temp2 = temp2.z_acc[temp2.action_flag == activity_id]
	norm_temp2 = np.sqrt(np.square(x_temp2)+np.square(y_temp2)+np.square(z_temp2))

	x_temp3 = temp3.x_acc[temp3.action_flag == activity_id]
	y_temp3 = temp3.y_acc[temp3.action_flag == activity_id]
	z_temp3 = temp3.z_acc[temp3.action_flag == activity_id]
	norm_temp3 = np.sqrt(np.square(x_temp3)+np.square(y_temp3)+np.square(z_temp3))

	x_temp4 = temp4.x_acc[temp4.action_flag == activity_id]
	y_temp4 = temp4.y_acc[temp4.action_flag == activity_id]
	z_temp4 = temp4.z_acc[temp4.action_flag == activity_id]
	norm_temp4 = np.sqrt(np.square(x_temp4)+np.square(y_temp4)+np.square(z_temp4))

	x_temp5 = temp5.x_acc[temp5.action_flag == activity_id]
	y_temp5 = temp5.y_acc[temp5.action_flag == activity_id]
	z_temp5 = temp5.z_acc[temp5.action_flag == activity_id]
	norm_temp5 = np.sqrt(np.square(x_temp5)+np.square(y_temp5)+np.square(z_temp5))

	x_temp6 = temp6.x_acc[temp6.action_flag == activity_id]
	y_temp6 = temp6.y_acc[temp6.action_flag == activity_id]
	z_temp6 = temp6.z_acc[temp6.action_flag == activity_id]
	norm_temp6 = np.sqrt(np.square(x_temp6)+np.square(y_temp6)+np.square(z_temp6))

	x_temp7 = temp7.x_acc[temp7.action_flag == activity_id]
	y_temp7 = temp7.y_acc[temp7.action_flag == activity_id]
	z_temp7 = temp7.z_acc[temp7.action_flag == activity_id]
	norm_temp7 = np.sqrt(np.square(x_temp7)+np.square(y_temp7)+np.square(z_temp7))

	x_temp8 = temp8.x_acc[temp8.action_flag == activity_id]
	y_temp8 = temp8.y_acc[temp8.action_flag == activity_id]
	z_temp8 = temp8.z_acc[temp8.action_flag == activity_id]
	norm_temp8 = np.sqrt(np.square(x_temp8)+np.square(y_temp8)+np.square(z_temp8))

	x_temp9 = temp9.x_acc[temp9.action_flag == activity_id]
	y_temp9 = temp9.y_acc[temp9.action_flag == activity_id]
	z_temp9 = temp9.z_acc[temp9.action_flag == activity_id]
	norm_temp9 = np.sqrt(np.square(x_temp9)+np.square(y_temp9)+np.square(z_temp9))

	x_temp10 = temp10.x_acc[temp10.action_flag == activity_id]
	y_temp10 = temp10.y_acc[temp10.action_flag == activity_id]
	z_temp10 = temp10.z_acc[temp10.action_flag == activity_id]
	norm_temp10 = np.sqrt(np.square(x_temp10)+np.square(y_temp10)+np.square(z_temp10))

	x_temp11 = temp11.x_acc[temp11.action_flag == activity_id]
	y_temp11 = temp11.y_acc[temp11.action_flag == activity_id]
	z_temp11 = temp11.z_acc[temp11.action_flag == activity_id]
	norm_temp11 = np.sqrt(np.square(x_temp11)+np.square(y_temp11)+np.square(z_temp11))
	
	x_temp12 = temp12.x_acc[temp12.action_flag == activity_id]
	y_temp12 = temp12.y_acc[temp12.action_flag == activity_id]
	z_temp12 = temp12.z_acc[temp12.action_flag == activity_id]
	norm_temp12 = np.sqrt(np.square(x_temp12)+np.square(y_temp12)+np.square(z_temp12))

	x_temp13 = temp13.x_acc[temp13.action_flag == activity_id]
	y_temp13 = temp13.y_acc[temp13.action_flag == activity_id]
	z_temp13 = temp13.z_acc[temp13.action_flag == activity_id]
	norm_temp13 = np.sqrt(np.square(x_temp13)+np.square(y_temp13)+np.square(z_temp13))

	x_temp14 = temp14.x_acc[temp14.action_flag == activity_id]
	y_temp14 = temp14.y_acc[temp14.action_flag == activity_id]
	z_temp14 = temp14.z_acc[temp14.action_flag == activity_id]
	norm_temp14 = np.sqrt(np.square(x_temp14)+np.square(y_temp14)+np.square(z_temp14))

	x_temp15 = temp15.x_acc[temp15.action_flag == activity_id]
	y_temp15 = temp15.y_acc[temp15.action_flag == activity_id]
	z_temp15 = temp15.z_acc[temp15.action_flag == activity_id]
	norm_temp15 = np.sqrt(np.square(x_temp15)+np.square(y_temp15)+np.square(z_temp15))
	
	ind_temp1 = temp1.index[temp1.action_flag == activity_id]/3120.0
	plt.subplot(5,3,1)
	plt.plot(ind_temp1,x_temp1,'r',ind_temp1,y_temp1,'g',ind_temp1,z_temp1,'b')
	
	ind_temp2 = temp2.index[temp2.action_flag == activity_id]/3120.0
	plt.subplot(5,3,2)
	plt.plot(ind_temp2,x_temp2,'r',ind_temp2,y_temp2,'g',ind_temp2,z_temp2,'b')
	
	ind_temp3 = temp3.index[temp3.action_flag == activity_id]/3120.0
	plt.subplot(5,3,3)
	plt.plot(ind_temp3,x_temp3,'r',ind_temp3,y_temp3,'g',ind_temp3,z_temp3,'b')
	
	ind_temp4 = temp4.index[temp4.action_flag == activity_id]/3120.0
	plt.subplot(5,3,4)
	plt.plot(ind_temp4,x_temp4,'r',ind_temp4,y_temp4,'g',ind_temp4,z_temp4,'b')
	
	ind_temp5 = temp5.index[temp5.action_flag == activity_id]/3120.0
	plt.subplot(5,3,5)
	plt.plot(ind_temp5,x_temp5,'r',ind_temp5,y_temp5,'g',ind_temp5,z_temp5,'b')
	
	ind_temp6 = temp6.index[temp6.action_flag == activity_id]/3120.0
	plt.subplot(5,3,6)
	plt.plot(ind_temp6,x_temp6,'r',ind_temp6,y_temp6,'g',ind_temp6,z_temp6,'b')
	
	ind_temp7 = temp7.index[temp7.action_flag == activity_id]/3120.0
	plt.subplot(5,3,7)
	plt.plot(ind_temp7,x_temp7,'r',ind_temp7,y_temp7,'g',ind_temp7,z_temp7,'b')
	
	ind_temp8 = temp8.index[temp8.action_flag == activity_id]/3120.0
	plt.subplot(5,3,8)
	plt.plot(ind_temp8,x_temp8,'r',ind_temp8,y_temp8,'g',ind_temp8,z_temp8,'b')
	
	ind_temp9 = temp9.index[temp9.action_flag == activity_id]/3120.0
	plt.subplot(5,3,9)
	plt.plot(ind_temp9,x_temp9,'r',ind_temp9,y_temp9,'g',ind_temp9,z_temp9,'b')
	
	ind_temp10 = temp10.index[temp10.action_flag == activity_id]/3120.0
	plt.subplot(5,3,10)
	plt.plot(ind_temp10,x_temp10,'r',ind_temp10,y_temp10,'g',ind_temp10,z_temp10,'b')
	
	ind_temp11 = temp11.index[temp11.action_flag == activity_id]/3120.0
	plt.subplot(5,3,11)
	plt.plot(ind_temp11,x_temp11,'r',ind_temp11,y_temp11,'g',ind_temp11,z_temp11,'b')
	
	ind_temp12 = temp12.index[temp12.action_flag == activity_id]/3120.0
	plt.subplot(5,3,12)
	plt.plot(ind_temp12,x_temp12,'r',ind_temp12,y_temp12,'g',ind_temp12,z_temp12,'b')
	
	ind_temp13 = temp13.index[temp13.action_flag == activity_id]/3120.0
	plt.subplot(5,3,13)
	plt.plot(ind_temp13,x_temp13,'r',ind_temp13,y_temp13,'g',ind_temp13,z_temp13,'b')
	
	ind_temp14 = temp14.index[temp14.action_flag == activity_id]/3120.0
	plt.subplot(5,3,14)
	plt.plot(ind_temp14,x_temp14,'r',ind_temp14,y_temp14,'g',ind_temp14,z_temp14,'b')
	
	ind_temp15 = temp15.index[temp15.action_flag == activity_id]/3120.0
	plt.subplot(5,3,15)
	plt.plot(ind_temp15,x_temp15,'r',ind_temp15,y_temp15,'g',ind_temp15,z_temp15,'b')
	
	plt.show()
	
trial1()