import os
import numpy as np
import matplotlib.pyplot as plt

##########################################################################################
##########################################################################################
##########################################################################################

def extents(f):
    delta = f[1] - f[0]
    return [f[0] - delta/2, f[-1] + delta/2]

def get_valid_index(i,j):
    temp1 = [[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
    temp2 = []
    for t in temp1:
        if min(t) >= 0 and max(t) < n:
            temp2.append(t)
    return temp2

def get_neighbours(temp,i,j):
    valid_ind = get_valid_index(i,j)
    nn = []
    for t in valid_ind:
        a,b = t
        nn.append(temp[a,b])
    return nn

def get_majority(nn):
    ones = sum(nn)
    alls = len(nn)
    zeros = alls-ones
    return zeros/alls,ones/alls

def make_new(temp):
    n,m = temp.shape
    backup = temp.copy()
    for i in range(n):
        for j in range(m):
            neighbours = get_neighbours(temp,i,j)
            p1,p2 = get_majority(neighbours)
            if p1 > my_thresh:
                backup[i,j] = 0
            elif p2 > my_thresh:
                backup[i,j] = 1            
    return backup

def single_plot(test):
    print(test)
    plt.imshow(test,interpolation = 'none')
    plt.show()

##########################################################################################
##########################################################################################
##########################################################################################

try:
    os.mkdir(os.getcwd()+'//portal//')
except:
    print('Folder already exists')

n = 75
n_trials = 50
my_thresh = 0.5
tt = []

x = np.array(range(n))
y = np.array(range(n))

data = np.random.binomial(1,0.5,size=(x.size,y.size))
single_plot(data)
proceed = input('Proceed?\n')

if proceed == 'y':
    for i in range(n_trials):
        frac = sum(sum(data))/n**2
        tt.append(frac)

        print('Iteration: {}, Fraction: {}'.format(i+1,frac))

        plt.imshow(data,interpolation = 'none')

        plt.savefig(os.getcwd()+'//portal//{}.png'.format(str(i+1).zfill(4)))
        plt.clf()

        data = make_new(data)

    plt.plot(tt)
    plt.show()

    os.system('python gif.py')
