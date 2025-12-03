import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def for_all_people2():
    activity_id = input('which activity ?? : ')
    for i in range(1,16):
        path = os.getcwd() +'\\data\\'+str(i)+'.csv'
        temp = pd.read_csv(path)
        temp.columns = ['index','x_acc','y_acc','z_acc','action_flag']
        x_temp = temp.x_acc[temp.action_flag == activity_id]
        y_temp = temp.y_acc[temp.action_flag == activity_id]
        z_temp = temp.z_acc[temp.action_flag == activity_id]
        norm_temp = np.sqrt(np.square(x_temp)+np.square(y_temp)+np.square(z_temp))

        ind_temp = temp.index[temp.action_flag == activity_id]/3120.0
        plt.subplot(5,3,i)
        plt.plot(ind_temp,x_temp,'r',ind_temp,y_temp,'g',ind_temp,z_temp,'b')

    plt.show()


for_all_people2()
