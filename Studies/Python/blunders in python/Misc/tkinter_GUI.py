import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import pandas as pd


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")
global f,a
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

def animate(j,number):
    print(number)
    temp = pd.read_csv('sampleText1.csv')
    xList = temp.iloc[:,0]
    yList = temp.iloc[:,1]
    a.clear()
    a.plot(xList, yList)

def ok(i,animate):
    print("value is", i)
    canvas = FigureCanvasTkAgg(f, root)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    ani = animation.FuncAnimation(f, animate,fargs = {i})

root = tk.Tk()
root.title("Main page")

container = tk.Frame(root)
container.pack(side="top", fill="both", expand = True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

label = tk.Label(root, text="Start Page", font=LARGE_FONT)
label.pack(pady=10,padx=10)

var = tk.StringVar(root)
var.set("one") # initial value
choices = [ "one","two"]
option = tk.OptionMenu(root,var,*choices)
option.pack()
button_ok = tk.Button(root, text="Select", command=lambda:ok(var.get(),animate)).pack()


root.mainloop()
