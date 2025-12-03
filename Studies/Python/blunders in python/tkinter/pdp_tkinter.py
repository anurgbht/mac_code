import random
import tkinter
import pylab as plt
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import GradientBoostingRegressor

############################################################################################################
############################################################################################################
############################################################################################################

class App:
    def __init__(self,master,clf,X,names):

        # Create a container
        frame = tkinter.Frame(master)

        var = tkinter.StringVar(frame)
        var.set("Which feature do you want on the y axis") # initial value
        choices = list(names)
        option_y = tkinter.OptionMenu(frame,var,*choices)
        option_y.pack(side = tkinter.LEFT)

        #slider = tkinter.Scale(frame, from_=-10, to=10, resolution=0.01, orient=tkinter.HORIZONTAL,length = 750)
        #slider.pack(side = tkinter.LEFT)
        
        self.button_select = tkinter.Button(frame,text="Select the value ?",
                                        command=lambda:self.select(var.get(),choices,clf,X))
        self.button_select.pack(side = tkinter.LEFT)

        fig = Figure()
        fig.suptitle("Partial dependence plot")
        
        b1 = [random.random() for x in range(1000)]
        
        ax = fig.add_subplot(111)
        ax.set_ylim(20,25)
        self.line, = ax.plot(range(len(b1)),b1)
        ax.grid(1)

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def select(self,beta_name,choices,clf,X):
        print(beta_name)
        index_val = choices.index(beta_name)
        yList = self.pdp_vis(clf,X,index_val)
        self.line.set_ydata(yList)
        self.canvas.draw()
        plt.plot(range(20))
        plt.show()
        

    def make_dat(self,x_avg,i,tt):
        ret_tt = []
        tt_temp = []
        for j in tt:
            ret_tt.append(x_avg)
        ret_tt = pd.DataFrame(ret_tt)
        ret_tt.iloc[:,i] = tt
        return ret_tt

    def pdp_vis(self,clf,X,i):
        x_avg = list(X.mean(axis=0))
        x_min = X.min(axis=0)
        x_max = X.max(axis=0)
        nx = len(x_avg)
        ns = 1000

        tt = np.linspace(x_min[i],x_max[i],ns)
        X_temp = self.make_dat(x_avg,i,tt)
        pred = clf.predict(X_temp)
        return pred
    
####################################################################################
####################################################################################
####################################################################################

dat = load_boston()
print(dat.data.shape)

X = dat.data
##X.columns = boston.feature_names
y = dat.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = GradientBoostingRegressor(n_estimators = 1000)
clf.fit(X_train,y_train)

root = tkinter.Tk()
root.title("My Visualization Tool")
app = App(root,clf,X,dat.feature_names)
root.mainloop()


