# general imports
import pandas as pd
import numpy as np
import all_trees as at

# sklearn imports
from sklearn.externals import joblib

####################################################################################################
####################################################################################################
####################################################################################################

def split_data(mod_dat):
    '''
	returns the corresponding subsets
	'''
    return id,y_1,y_2,X_1,X_2

def my_predict_raw_single(X):
    X = list(X.iloc[0,:])
    
    X = [(xt-mt)/np.sqrt(vt) for xt,mt,vt in zip(X,at.mean_val,at.var_val)]
    pred = 0
    for est in at.all_pred_func:
        pred += est(X)
    pred = at.ybar + at.lam*pred
    
    return pred
        

def my_test(mod_dat,model_save_path,vessel):
    print("Begin testing.\n")
    id,y_1,y_2,X_1,X_2 = split_data(mod_dat)
    
    ###################################################################################################
    
    pred_1 = my_predict_raw_single(X_1)
    ###################################################################################################
    
    pred_2 = my_predict_raw_single(X_2)
    ###################################################################################################
    
    return pred_1,pred_2
    
