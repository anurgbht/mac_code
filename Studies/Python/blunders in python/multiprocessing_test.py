'''
Aim of the function was to determine if python3 multiprocessing performed
differently on ubuntu as compared to windows

Conclusion: it is the same
One change
in ubuntu one can run the code without "if __name__ == '__main__':" snippet
'''

import os
import sys
import time
import multiprocessing as mp

def find_cube(x):
    time.sleep(3)
    return x**3

if __name__ == '__main__':

    st = time.time()
    print('Hello.')
    with mp.Pool(processes = 4) as pool:
        #print('Inside.')
        q = [pool.apply_async(find_cube,args=(x,)) for x in range(12)]
        p = [x.get() for x in q]

    print(time.time()-st)

    print(p)
