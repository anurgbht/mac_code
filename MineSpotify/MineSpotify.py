import random

def calc_stat(left,right):
    s = 0
    for x in left:
        for y in right:
            if x>y:
                s +=1
            elif x==y:
                s += 0.5
            else:
                s += 0
    return s

tt1 = [random.normalvariate(7,5) for x in range(20)]
tt2 = [random.normalvariate(5,1) for x in range(20)]

print(calc_stat(tt1,tt2))