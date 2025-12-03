import numpy as np
import pandas as pd
import random
import matplotlib as plt

def my_simu(data):
    # generating a temperory structure so that the original does not get over-written
    sequence=[]
    for i in range(0,len(data)):
        sequence.append((data[i]))
        
    for i in range(0,len(sequence)-1):
        if sequence[i]<sequence[i+1]:
            sequence[i+1] = sequence[i]

    outvar=[]
    outvar.append((len(set(sequence)),((sum(sequence))/(len(sequence)))))
    return outvar

no_cars = int(input('Tell me, how many cars do you want ? '))

print('okay ',no_cars,' it is.')

cars = np.array(range(1,no_cars+1))

no_iter = 10

iteration_val=[]

for i in range(0,no_iter):
    random.shuffle(cars)
    print(cars)
    temp = my_simu(cars)
    iteration_val.append(temp)

print(iteration_val)

input()
