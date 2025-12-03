import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

t = np.linspace(-math.pi,math.pi,5000)

global x1,x2,y1,y2

y1 = [math.sin(tt) for tt in t]
x1 = [math.cos(tt) for tt in t]
y2 = [math.sin(tt) + 5 for tt in t]
x2 = [math.cos(tt) + 5 for tt in t]

x1 = pd.DataFrame(x1)
y1 = pd.DataFrame(y1)
y2 = pd.DataFrame(y2)
x2 = pd.DataFrame(x2)

fig,ax = plt.subplots()
ax.axis([-3,8,-3,8])
plt.grid(1)
ax.plot(x1,y1)

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    global coords
    coords = [ix, iy]
    coords = np.array(coords)
    print(coords)

    p1=coords[0]
    p2=coords[1]

    tx1 = (p1 + np.sqrt((np.square(p2)*(np.square(p1)+np.square(p2)))-(np.square(p2))))/(np.square(p1)+np.square(p2))
    ty11 = np.sqrt(1-np.square(tx1))
    ty12 = -np.sqrt(1-np.square(tx1))

    tempdp = (abs((p1-tx1)*tx1 + (p2-ty11)*ty11) - abs((p1-tx1)*tx1 + (p2-ty12)*ty12))
    if tempdp > 0:
        ty1 = ty12
    else:
        ty1 = ty11
    
    tx2 = (p1 - np.sqrt((np.square(p2)*(np.square(p1)+np.square(p2)))-(np.square(p2))))/(np.square(p1)+np.square(p2))
    ty21 = np.sqrt(1-np.square(tx2))
    ty22 = -np.sqrt(1-np.square(tx2))

    tempdp = (abs((p1-tx2)*tx2 + (p2-ty21)*ty21) - abs((p1-tx2)*tx2 + (p2-ty22)*ty22))
    if tempdp > 0:
        ty2 = ty22
    else:
        ty2 = ty21
    
    a1=coords
    temp2=[tx1,ty1]
    a2=np.array(temp2)
    xall = np.linspace(-3,8,100)
    yall1 = []

    prod1 = ((a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(5-a1[0]))-5)*((a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(0-a1[0]))-0)

    for x in xall:
        temp = a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(x-a1[0])
        yall1.append(temp)

    temp2=[tx2,ty2]
    a2=np.array(temp2)
    xall = np.linspace(-3,8,100)
    yall2 = []

    prod2 = ((a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(5-a1[0]))-5)*((a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(0-a1[0]))-0)

    for x in xall:
        temp = a1[1] + ((a2[1]-a1[1])/(a2[0]-a1[0]))*(x-a1[0])
        yall2.append(temp)

    if prod1 < 0:
        yall = yall1
        temp2=[tx1,ty1]
        a2=np.array(temp2)
        m = (a2[1]-a1[1])/(a2[0]-a1[0])
    elif prod2 < 0:
        yall = yall2
        temp2=[tx2,ty2]
        a2=np.array(temp2)
        m = (a2[1]-a1[1])/(a2[0]-a1[0])
    else:
        print('both lines are bad')

    alpha = 4*m*m-4
    beta = 4*m*(10*m+20)
    gamma = np.square(10*m+20) + 4*49

    c = (beta+np.sqrt(np.square(beta) - 4*alpha*gamma))/(2*alpha)
    print(c,m)
    yall3=[]
    for x in xall:
        temp = c + m*(x)
        yall3.append(temp)
    fig,ax = plt.subplots()
    plt.grid(1)
    ax.plot(xall,yall,xall,yall3,x1,y1,x2,y2)
    plt.show()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
