import numpy as np

group1 = [[1, 2], [1, 4], [5, 4]]
group2 = [[3, 1], [3, 2]]


def myDist(x, y):
    return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

N = 6
tt = np.zeros(shape=(N, N))

for i in range(N):
    for j in range(N):
        minGroup1 = min([myDist([i + 1, j + 1], x) for x in group1])
        minGroup2 = min([myDist([i + 1, j + 1], x) for x in group2])
        if minGroup1 > minGroup2:
            assignedClass = 2
        else:
            assignedClass = 1
        tt[i, j] = assignedClass
print(tt)
