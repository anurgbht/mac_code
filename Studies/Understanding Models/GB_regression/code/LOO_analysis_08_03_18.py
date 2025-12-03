import os
import numpy as np
import pandas as pd
import pylab as plt
from sklearn import tree
import pydotplus
import BOF_module_08_03_18 as bof

##########################################################################################################
##########################################################################################################
##########################################################################################################

def main_test():
    data_path = "..."
    model_save_path = "..."
    mod_dat = pd.read_excel('...')

    pred_lime,pred_ore,pred_oxy = bof.my_test(mod_dat,model_save_path,0)
    print("Predictions :\n Lime : {0}, Ore : {1}, Oxygen : {2}".format(pred_lime,pred_ore,pred_oxy))

def main_train():

    CV = 2
    print('Training for CV : {0}'.format(CV))
    mod_path = "..."
    model_save_path = "..."
    mod_dat = pd.read_excel('...')
    mod_dat = mod_dat.dropna().reset_index().drop('index',1)
    print("Size of the dataset : ",mod_dat.shape)
    scaler_lime,clf_lime,scaler_ore,clf_ore,scaler_oxy,clf_oxy = bof.my_train(mod_dat,model_save_path)

    return scaler_lime,clf_lime,scaler_ore,clf_ore,scaler_oxy,clf_oxy

    

##########################################################################################################
##########################################################################################################
##########################################################################################################

scaler_lime,clf_lime,scaler_ore,clf_ore,scaler_oxy,clf_oxy = main_train()

