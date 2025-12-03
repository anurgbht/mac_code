import os
from sklearn.externals import joblib
from sklearn import tree

##########################################################################################################
##########################################################################################################
##########################################################################################################

def make_text(leaf_node,leaf_descr,node_descr,parent_child,child_parent,fw):
    value = leaf_descr[leaf_node]
    c = leaf_node
    flag = 1
    condition = "\n\tif ( "
    while flag == 1:
        try:
            p = child_parent[c]
            if parent_child[p].index(c) == 1:
                condition += "(" + node_descr[p].split("<=")[0] + " > " + node_descr[p].split("<=")[1] + ") and "
            else:
                condition += "(" + node_descr[p] + ") and "
            c = p
        except:
            flag = 0
    condition = condition[:-4] + ") : \n\t\t" + "pred = " + str(leaf_descr[leaf_node])
    fw.write(condition)

def make_beginning(fw,dot_file_name):
    tt = "\ndef " + dot_file_name.split('.')[0] + "(X) :"
    fw.write(tt)

def make_end(fw):
    tt = "\n\treturn pred\n\n"
    fw.write(tt)

def make_dot_dat(clf):
    dot_path = "..."
    for file in os.listdir(dot_path):
        os.remove(dot_path+file)
    count = 0
    for t in clf.estimators_:
        t = t[0]
        count += 1
        name = 'T_'+str(count).zfill(4)
        tree.export_graphviz(t,out_file = dot_path+name+'.dot')
    
def make_if_else():

    dot_path = "..."
    write_path = "..."
    os.chdir(dot_path)

    fw = open(write_path+"T_all_trees.py","a+")
    all_pred_func = "\n\nall_pred_func = ["

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
        all_pred_func +=  dot_file_name.split('.')[0] + ','

    all_pred_func = all_pred_func[:-1]
    all_pred_func += "]\n"
    fw.write(all_pred_func)
    fw.close()

def write_gen(save_path,write_path):
    clf = joblib.load(save_path+vessel+"/ore_GBR.pkl")
    scaler = joblib.load(save_path+vessel+"/ore_scaler.pkl")
    fw = open(write_path+"T_all_trees.py","w")
    fw.write("\nmean_val = "+str(scaler.mean_.tolist()))
    fw.write("\nvar_val = "+str(scaler.var_.tolist()))
    fw.write("\nybar = "+str(clf.init_.mean))
    fw.write("\nlam = "+str(clf.get_params()['learning_rate']))
    fw.close()
    make_dot_dat(clf)
    make_if_else()


##########################################################################################################
##########################################################################################################
##########################################################################################################

'''
for each vessel and model
write general data
write dat data
convert dot data to if else
'''

save_path = "..."
write_path = "..."

write_gen(save_path,write_path)
























