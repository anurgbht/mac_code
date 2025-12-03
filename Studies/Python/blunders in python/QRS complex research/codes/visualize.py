import pandas as pd
import wfdb
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
from matplotlib  import cm
from collections import Counter
import scipy
##from mpl_toolkits.mplot3d import Axes3D

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

