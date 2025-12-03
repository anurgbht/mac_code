## trial for signal processing

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wfdb
import matplotlib.pyplot as plt
from matplotlib  import cm
from collections import Counter
##
##
##t = np.linspace(-1, 1, 201)
##x = (np.sin(2*np.pi*0.75*t*(1-t) + 2.1) + 0.1*np.sin(2*np.pi*1.25*t + 1)
##     + 0.18*np.cos(2*np.pi*3.85*t))
##xn = x + np.random.randn(len(t)) * 0.08
##

p='207'
print(p)
sig, fields = wfdb.rdsamp(p)
annsamp, anntype, subtype, chan, num, aux, annfs = wfdb.rdann(p, 'atr')
##wfdb.plotwfdb(sig, fields)

print(len(anntype))
print(Counter(anntype).keys())
print(Counter(anntype).values())

field='!'
if anntype.count(field)>0:
    if anntype.count(field)> 3:
        i=anntype.index(field,3)
        print(i)
        sig, fields = wfdb.rdsamp(p,sampfrom=annsamp[i]-150, sampto=annsamp[i]+150)
        wfdb.plotwfdb(sig, fields)
    else:
        i=anntype.index(field)
        print(i)
        sig, fields = wfdb.rdsamp(p,sampfrom=annsamp[i]-150, sampto=annsamp[i]+150)
        wfdb.plotwfdb(sig, fields)
else:
    print('field absent')

sig=pd.DataFrame(sig)
xn = sig.iloc[:,0]
t=np.linspace(0,10,len(sig))

b, a = signal.butter(3, 0.05)

zi = signal.lfilter_zi(b, a)
z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

y = signal.filtfilt(b, a, xn)

plt.figure
plt.plot(t, xn, 'b', alpha=0.75)
plt.plot(t, y, 'k')
plt.legend(('noisy signal', 'filtered'), loc='best')
plt.grid(True)
plt.show()
