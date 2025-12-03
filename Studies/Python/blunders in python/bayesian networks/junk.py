import pylab as plt
import numpy as np


def calc_prob(x):
    return (1-x)/(2-x)

tt = np.linspace(0,1,10)
prob = [calc_prob(x) for x in tt]

plt.plot(tt,prob,'.')
plt.grid(1)
plt.show()
