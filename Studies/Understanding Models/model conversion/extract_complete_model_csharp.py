import os
from sklearn.externals import joblib
from sklearn import tree
##import numpy as np
##import pandas as pd
##import pylab as plt
##from sklearn import tree
##import pydotplus
##import BOF_module_08_03_18 as bof

##########################################################################################################
##########################################################################################################
##########################################################################################################

def make_text(leaf_node,leaf_descr,node_descr,parent_child,child_parent,fw):
    value = leaf_descr[leaf_node]
    c = leaf_node
    flag = 1
    condition = "\n\t\tif ( "
    while flag == 1:
        try:
            p = child_parent[c]
            if parent_child[p].index(c) == 1:
                condition += "(" + node_descr[p].split("<=")[0] + " > " + node_descr[p].split("<=")[1] + ") && "
            else:
                condition += "(" + node_descr[p] + ") && "
            c = p
        except:
            flag = 0
    condition = condition[:-4] + "){ \n\t\t\t" + "pred = " + str(leaf_descr[leaf_node]) + ";\n\t\t}"
    fw.write(condition)

def make_beginning(fw,dot_file_name):
    tt = "\n\tdouble " + dot_file_name.split('.')[0] + "(double[] X) {\n\t\tdouble pred = 0;"
    fw.write(tt)

def make_end(fw):
    tt = "\n\t\treturn pred;\n\t}\n"
    fw.write(tt)

def make_dot_dat(clf,vessel,model):
    dot_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/trees/"
    for file in os.listdir(dot_path):
        os.remove(dot_path+file)
    count = 0
    for t in clf.estimators_:
        t = t[0]
        count += 1
        name = vessel+'_'+model+'_'+str(count).zfill(4)
        tree.export_graphviz(t,out_file = dot_path+name+'.dot')
    
def make_if_else(model,vessel):

    dot_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/trees/"
    write_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/if_else_trees_tuned_csharp/"
    os.chdir(dot_path)

    fw = open(write_path+vessel+"_"+model+"_all_trees.cs","w")
    fw.write("class Program{\n")
    all_pred_func = ""

    for dot_file_name in os.listdir():
        f = open(dot_file_name,"r")
        parent = []
        child = []
        leaves = []
        node_descr = {}
        leaf_descr = {}
        parent_child = {}
        child_parent = {}
        for line in f.readlines():
            if "->" in line:
                p = int(line.split("->")[0])
                c = int(line.split("->")[1][:3])
                parent.append(p)
                child.append(c)
                if p in parent_child:
                    parent_child[p].append(c)
                else:
                    parent_child[p] = [c]
                child_parent[c] = p
            if 'label="X[' in line:
                node_descr[int(line.split("[")[0])] = line.split('\\nfriedman_mse')[0].split('"')[-1]
            if 'label="friedman_mse' in line:
                leaf_descr[int(line.split("[")[0])] = float(line.split("value =")[-1].split('"')[0])
                
        for node in child:
            if node not in parent:
                leaves.append(node)

        make_beginning(fw,dot_file_name)
        for leaf in leaves:
            make_text(leaf,leaf_descr,node_descr,parent_child,child_parent,fw)
        make_end(fw)
        all_pred_func +=  'program.' + dot_file_name.split('.')[0] + '(X) + '

    all_pred_func = all_pred_func[:-1]
    all_pred_func += ";\n"
    fw.close()
    return all_pred_func

def write_gen(vessel,model,save_path,write_path):
    if model == 'ore':
        clf = joblib.load(save_path+vessel+"/ore_GBR.pkl")
        scaler = joblib.load(save_path+vessel+"/ore_scaler.pkl")
    elif model == 'oxy':
        clf = joblib.load(save_path+vessel+"/oxy_GBR.pkl")
        scaler = joblib.load(save_path+vessel+"/oxy_scaler.pkl")
    make_dot_dat(clf,vessel,model)
    all_pred_func = make_if_else(model,vessel)
    fw = open(write_path+vessel+"_"+model+"_all_trees.cs","a+")
    fw.write("\n\tstatic void Main()\n\t{")
    fw.write("\n\t\tdouble[] mean_val = {"+str(scaler.mean_.tolist())[1:-1]+"};")
    fw.write("\n\t\tdouble[] var_val = {"+str(scaler.var_.tolist())[1:-1]+"};")
    fw.write("\n\t\tdouble ybar = "+str(clf.init_.mean)+";")
    fw.write("\n\t\tdouble lam = "+str(clf.get_params()['learning_rate'])+";")
    fw.write("\n\t\tdouble[] X = { 1.2,1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2};")
    fw.write("\n\t\tfor (int i = 0; i <"+str(len(scaler.var_.tolist()))+";i++) { \n\t\tX[i] = (X[i] - mean_val[i]) / System.Math.Sqrt(var_val[i]);\n\t\t}")
    fw.write("\n\t\tProgram program = new Program();")
    fw.write("\n\t\tdouble final_prediction = ybar + lam *("+all_pred_func[:-3]+");")
    fw.write("\n\t}")
    fw.write("\n}")
    fw.close()

    return clf,scaler
    


##########################################################################################################
##########################################################################################################
##########################################################################################################

'''
for each vessel and model
write general data
write dat data
convert dot data to if else
'''

save_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/saved_clf_tuned/"
write_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/if_else_trees_tuned_csharp/"

vessels = ['CV2']
models = ['ore']

for  vessel in vessels:
    for model in models:
        clf,scaler = write_gen(vessel,model,save_path,write_path)


