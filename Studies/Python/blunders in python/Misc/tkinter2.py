import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import pandas as pd
import numpy as np
import my_functions as mf
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import random

def include_tree(row):
    x2 = row[1]
    x6 = row[5]
    x7 = row[6]
    x8 = row[7]
    x13 = row[12]

    if x2 <= 6.85:
        if x7 <= 0.9846:
            if x6 <= 1.0045:
                tt = 'A'
            elif x6 > 1.0045:
                tt = 'B'
        elif x7 > 0.9846:
            tt = 'C'
    elif x2 > 6.85:
        if x13 <= 9.45:
            tt = 'D'
        elif x13 > 9.45:
            tt = 'E'
    return tt


def subs_WOE(row):
    temp = woe_table.loc[woe_table.iloc[:,0] == row.iloc[-1],1]
    return temp



os.chdir('D:/Public/Personal/blunders in python')
class App:
    def __init__(self, master):

        os.chdir('D:/Confidential/Projects/Steel/LD2 BDS/prelim_analysis/data/constructed data/')
        temp = pd.read_csv('data_dump_24_3_17.csv')
        print(temp.shape)
        temp = temp.dropna()
        print(temp.shape)

        X_all_left = pd.DataFrame(temp.iloc[:,0:20])
        X_all_trigger = pd.DataFrame(temp.iloc[:,20:40])
        X_all_right = pd.DataFrame(temp.iloc[:,40:60])
        Y_all_clean = temp.iloc[:,60]
        index_file_clean = temp.iloc[:,61]

        X_all_trigger.columns = ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10","X11","X12","X13","X14","X15","X16","X17","X18","X19","X20"]
        X_all_left.columns = ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10","X11","X12","X13","X14","X15","X16","X17","X18","X19","X20"]
        X_all_right.columns = ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10","X11","X12","X13","X14","X15","X16","X17","X18","X19","X20"]

        print(X_all_trigger.shape,' : Size of all X trigger')
        print(X_all_left.shape,' : Size of all X left')
        print(X_all_right.shape,' : Size of all X right')
        print(Y_all_clean.shape,' : Size of all Y')
        print(index_file_clean.shape,' : Shape of index file')

        ##from sklearn import tree
        ##import pydotplus
        ##clf = tree.DecisionTreeClassifier(min_samples_leaf=25,max_depth = 7)
        ##clf = clf.fit(X_all_trigger,Y_all_clean)
        ##dot_data = tree.export_graphviz(clf, out_file=None)
        ##graph = pydotplus.graph_from_dot_data(dot_data)
        ##pdf_name = "temp_vis_27_3_17" + ".pdf"
        ##graph.write_pdf(pdf_name)

        temp = X_all_trigger.apply(include_tree,axis=1)

        data_logit = pd.concat([X_all_trigger,temp],axis=1)

        print(X_all_trigger.shape)
        print(data_logit.shape)

        global woe_table
        woe_table = mf.calc_WOE(data_logit.iloc[:,-1],Y_all_clean)

        temp2 = data_logit.apply(subs_WOE,axis=1)

        # just to make sure everything is going okay
        temp3 = pd.concat([temp2,data_logit.iloc[:,-1]],axis=1)

        data_logit = pd.concat([X_all_trigger,temp2],axis=1)

        clf_logit_trigger = LogisticRegression()
        clf_logit_trigger =clf_logit_trigger.fit(data_logit,Y_all_clean)

        # Create a container
        frame = tkinter.Frame(master)

        var = tkinter.StringVar(frame)
        var.set("Which file do you want") # initial value
        choices = [ "one","two"]
        option = tkinter.OptionMenu(frame,var,*choices)
        option.pack()

        label = tkinter.Label(frame, text = "what beta value do you want ?")
        label.pack()
        entry = tkinter.Entry(frame)
        entry.pack()

        self.button_select = tkinter.Button(frame,text="Select the value ?",
                                        command=lambda:self.select(var.get(),entry.get()))
        self.button_select.pack()

        fig = Figure()
        ax = fig.add_subplot(111)
        self.line, = ax.plot(range(10))

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def select(self,beta_name,beta_value):
        print(beta_name,beta_value)
        if beta_name == 'one':
            temp = pd.read_csv('sampleText1.csv')
            xList = temp.iloc[:,0]
            yList = temp.iloc[:,1]
        elif beta_name == 'two':
            temp = pd.read_csv('sampleText2.csv')
            xList = temp.iloc[:,0]
            yList = temp.iloc[:,1]
        self.line.set_ydata(yList)
        self.line.set_xdata(xList)
        self.canvas.draw()

root = tkinter.Tk()
app = App(root)
root.mainloop()
