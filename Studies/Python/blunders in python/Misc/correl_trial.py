import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rnd


for i in range(50000):
    print(i)
    n = 50
    m=int(n/2)
    index = list(range(n))
    rnd.shuffle(index)
    a = [rnd.gauss(0,1) for x in range(n)]
    temp = [rnd.gauss(0,1) for x in range(n)]
    b = [x+(y/100) for x,y in zip(a, temp)]
    a1 = [a[x] for x in index[:m]]
    b1 = [b[x] for x in index[:m]]
    a2 = [a[x] for x in index[m:]]
    b2 = [b[x] for x in index[m:]]
    tt = abs(np.corrcoef([a],[b])[0][1])
    t1 = abs(np.corrcoef([a1],[b1])[0][1])
    t2 = abs(np.corrcoef([a2],[b2])[0][1])
    if (tt > t1) & (tt > t2) & ((tt - max(t1,t2)) > 0.05):
        plt.subplot(2,2,1)
        plt.scatter(a,b)
        plt.title('Correlation Overall = '+str(tt))

        plt.subplot(2,2,2)
        plt.scatter(a1,b1)
        plt.title('Correlation A = '+str(t1))

        plt.subplot(2,2,3)
        plt.scatter(a2,b2)
        plt.title('Correlation B = '+str(t2))

        plt.subplot(2,2,4)
        plt.hist([a,b])
        plt.title('Histogram')
        plt.show()
