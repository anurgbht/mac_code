from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pylab as plt

def make_ann(X,y):
    act = 'relu'
    
    model = Sequential()
    model.add(Dense(X.shape[1], input_dim=X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(X.shape[1], activation=act))
    model.add(Dense(1, activation='linear'))

    # compile the keras model
    model.compile(loss='mse', optimizer='adam', metrics=['mae','mse'])

    # fit the keras model on the dataset
    model.fit(X, y, epochs=2000, batch_size=int(X.shape[0]/10), verbose=1)

    return model


import random
n = 100000

x = [[random.normalvariate(0,1),random.normalvariate(0,1),random.normalvariate(0,1)] for x in range(n)]

y = [sum(map(lambda x: x**2,t)) for t in x]

x = np.array(x)
y = np.array(y)

clf = make_ann(x,y)

plt.plot(clf.predict(x),y,'.')
plt.grid(1)
plt.show()

input('Wait')
