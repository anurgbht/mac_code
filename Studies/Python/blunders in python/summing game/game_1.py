import pandas as pd
import numpy as np

N=30
p=8
win = 0
cumsum = 0
my_turn = 6
wanna_play = input('Do you want to play the game ? Enter y or n ! \n')
if wanna_play == 'y':
    print('Let us play')
    print('Instructions')
    while win == 0:
        print('I entered : ',my_turn)
        if cumsum == N:
            print('I win !')
            break
        your_turn = input('Enter the digit, please ensure it is between 1 and 7 (including) \n')
        if int(your_turn) in [1,2,3,4,5,6,7]:
            cumsum = cumsum + my_turn
            if cumsum == N:
                print('I win !')
                break
            cumsum = cumsum + int(your_turn)
            if cumsum == N:
                print('You win')
                break
            my_turn = p - int(your_turn)
            print('The cumulative sum is : ', cumsum)
        else:
            print('Incorrect input, try again ! The cumulative sum will not change')
            
elif wanna_play == 'n':
    print('Exiting')
    win = 1
else:
    print('Incorrect input, enter y or n !')
