##python -m pip install matplotlib (run the code on the left to install matplotlib from cmd D:)

import numpy as numpy
import pandas as pandas
import dateutil as dateutil
##import openpyxl as openpyxl
import datetime as datetime
##import xlrd
import array
import math
import matplotlib.pyplot as plt
import os
import re
import pydot
import pydotplus

##Dat1_EngRun0 = pandas.read_csv("D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/SatrajitKar/TataMotors/Telematics/Python_WS/telematics_data/Decision Tree Data/dt_cleandata_0.csv", header=0, sep=',', parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
##df1 = Dat1_EngRun0.drop(['V1','V2','severity_flag'], 1)
##df2 = df1.fillna(-99999)

dataset = [[0,20,12,1],
[0,0,30,1],
[-99999,15,20,1],
[-99999,5,5,0],
[3,6,12,0],
[4,3,13,0],
[5,9,4,0],
[6,4,6,0],
[20,0,2,0]]

q = 0
for row in dataset:
        row.insert(0,q)
        q = q + 1

col_list = ['Index','Var1','Var2','Var3','Target']

node_cntr = 0
tree_list_orig = list()
tree_list_custom = list()
successor_tree = list()
plot_node_list = list()
tree_lineage_orig = [""]*len(dataset)
tree_lineage_custom = [""]*len(dataset)
##col_list = list()
##for col in dataset:
##        col_list.append(col)

root_size = len(dataset)

# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset, node_cntr, add_lineage_ind, orig_tree_ind):
        global tree_lineage_orig
        global tree_lineage_custom
        left, right = list(), list()
        for row in dataset:
                if add_lineage_ind == 1:
                                if orig_tree_ind == 1:
                                        tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_"
                                else:
                                        tree_lineage_custom[row[0]] = tree_lineage_custom[row[0]] + str(node_cntr) + "_"
                                        
                if row[index] <= value:
                        left.append(row)                                                                                
                else:
                        right.append(row)

        return left, right
 
# Calculate the Gini index for a split dataset
def gini_index(groups, class_values):
        gini = 0.0
        for class_value in class_values:
                for group in groups:
                        size = len(group)
                        if size == 0:
                                continue
                        proportion = [row[-1] for row in group].count(class_value) / float(size)
                        gini += (proportion * (1.0 - proportion))
        return gini
 
# Select the best split point for a dataset
def get_split(dataset, node_cntr, orig_tree_ind):
        full_pop = len(dataset)
        prop1 = [row[-1] for row in dataset].count(1) / float(full_pop)
        perc_pop = float(full_pop)/float(root_size)
        gini_list = list()        
        class_values = list(set(row[-1] for row in dataset))
        b_index, b_value, b_score, b_groups = 999, 999, 999, None
        for index in range(1, len(dataset[0])-1):
                for row in dataset:
                        groups = test_split(index, row[index], dataset, node_cntr, 0, orig_tree_ind)
                        gini = gini_index(groups, class_values)
                        gini_list.append([index, row[index], gini])
                        if gini < b_score:
                                b_index, b_value, b_score, b_groups = index, row[index], gini, groups

        test_split(b_index, b_value, dataset, node_cntr, 1, orig_tree_ind)
        t1 = sorted(gini_list)
        t2 = [t1[i] for i in range(len(t1)) if i == 0 or t1[i] != t1[i-1]]
        t3 = sorted(t2,key=lambda l:l[2])
        t4 = t3[:10]
        left_size = len(b_groups[0])
        right_size = len(b_groups[1])
        
        if left_size ==0:
                left_prop1 = -99999
        else:
                left_prop1 = [row[-1] for row in b_groups[0]].count(1) / float(left_size)

        if right_size ==0:
                right_prop1 = -99999
        else:
                right_prop1 = [row[-1] for row in b_groups[1]].count(1) / float(right_size)
            
        return {'full_pop':full_pop, 'prop1':prop1, 'perc_pop':perc_pop, 'index':b_index, 'col_name':col_list[b_index], 'value':b_value, 'groups':b_groups, 'gini_list':t4, 'left_size':left_size, 'left_prop1':left_prop1, 'right_size':right_size, 'right_prop1':right_prop1}
    
 
# Create a terminal node value
def to_terminal(group):
        outcomes = [row[-1] for row in group]
        return max(set(outcomes), key=outcomes.count)
 
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth, parent_node):
        left, right = node['groups']
        global tree_lineage_orig
        global node_cntr
        global tree_list_orig
        del(node['groups'])
        
        # check for a no split
        if not left or not right:
                node['left'] = node['right'] = to_terminal(left + right)
                if not left:
                    node_cntr = node_cntr + 1
                    temp_node = get_split(right, node_cntr, 1)
                    tree_list_orig.append([parent_node,node_cntr,'R',-99,-99,'T', temp_node['gini_list']])
                    for row in right:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_" 
                elif not right:
                    node_cntr = node_cntr + 1
                    temp_node = get_split(left, node_cntr, 1)
                    tree_list_orig.append([parent_node,node_cntr,'L',-99,-99,'T', temp_node['gini_list']])
                    for row in left:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_" 
                return
            
        # check for max depth
        if depth >= max_depth:
                node['left'], node['right'] = to_terminal(left), to_terminal(right)
                node_cntr = node_cntr + 1
                temp_node = get_split(left, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'L',-99,-99,'T', temp_node['gini_list']])
                for row in left:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_"
                node_cntr = node_cntr + 1
                temp_node = get_split(right, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'R',-99,-99,'T', temp_node['gini_list']])
                for row in right:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_"
                return
            
        # process left child
        if len(left) <= min_size:
                node['left'] = to_terminal(left)
                node_cntr = node_cntr + 1
                temp_node = get_split(left, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'L',-99,-99,'T', temp_node['gini_list']])
                for row in left:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_"
        else:
                node_cntr = node_cntr + 1
                node['left'] = get_split(left, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'L',node['left']['index'], node['left']['value'], 'NT', node['left']['gini_list']])
                split(node['left'], max_depth, min_size, depth+1, node_cntr)
                
        # process right child
        if len(right) <= min_size:
                node['right'] = to_terminal(right)
                node_cntr = node_cntr + 1
                temp_node = get_split(right, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'R',-99,-99,'T', temp_node['gini_list']])
                for row in right:
                            tree_lineage_orig[row[0]] = tree_lineage_orig[row[0]] + str(node_cntr) + "_"
        else:
                node_cntr = node_cntr + 1
                node['right'] = get_split(right, node_cntr, 1)
                tree_list_orig.append([parent_node,node_cntr,'R',node['right']['index'], node['right']['value'], 'NT', node['right']['gini_list']])
                split(node['right'], max_depth, min_size, depth+1, node_cntr)
 
# Build a decision tree
def build_tree(train, max_depth, min_size):
        global node_cntr
        node_cntr = node_cntr + 1        
        root = get_split(train, node_cntr, 1)
        tree_list_orig.append([0,node_cntr,'P',root['index'], root['value'], 'NT', root['gini_list']])
        split(root, max_depth, min_size, 1, node_cntr)
        return root
 
# Print a decision tree
def print_tree(node, size, prop1, depth=0):
        if isinstance(node, dict):
                print('%s[X%d (%s) <= %.3f], Size: %d, Perc of Root Pop: %.3f, Prop1: %.3f' % (depth*' ', (node['index']+1), node['col_name'], node['value'], node['full_pop'], node['perc_pop'], node['prop1']))
                print(pandas.DataFrame(node['gini_list']))
                print_tree(node['left'], node['left_size'], node['left_prop1'], depth+1)
                print_tree(node['right'], node['right_size'], node['right_prop1'], depth+1)
        else:
                print('%s[%d], Size: %d, Perc of Root Pop: %.3f, Prop1: %.3f' % ((depth*' ', node, size, size/root_size, prop1)))


def plot_tree(tree_in_list, plot_node_list, tree_name):
        
        graph = pydot.Dot(graph_type='digraph')

        for i in range(len(plot_node_list)):
                graph.add_node(plot_node_list[i][1])
                
        for i in range(len(tree_in_list)):
                from_node = tree_in_list[i][0]
                to_node = tree_in_list[i][1]

                split_var = -1
                split_val = -1
                for z in range(len(tree_in_list)):
                        if tree_in_list[z][1] == from_node:
                                split_var = tree_in_list[z][3]
                                split_val = tree_in_list[z][4]
                                
                
                temp1 = -1
                temp2 = -1
                for j in range(len(plot_node_list)):
                        if plot_node_list[j][0] == from_node and from_node > 0:
                                temp1 = j
                        if plot_node_list[j][0] == to_node:
                                temp2 = j
                if temp1 >= 0 and temp2 >= 0:
                        if tree_in_list[i][2] == 'L':
                                graph.add_edge(pydot.Edge(plot_node_list[temp1][1], plot_node_list[temp2][1], label = '%s <= %.3f' % (col_list[split_var], split_var)))
                        if tree_in_list[i][2] == 'R':
                                graph.add_edge(pydot.Edge(plot_node_list[temp1][1], plot_node_list[temp2][1], label = '%s > %.3f' % (col_list[split_var], split_var)))
                
##        graph.write_pdf('Tree_V1.pdf')

        return graph

def populate_tree_from_list(tree_in_list, tree_dat, node_ind):
    global tree_lineage_custom
    global plot_node_list
    
    node_pop = len(tree_dat)
    if node_pop > 0:
        node_prop1 = [row[-1] for row in tree_dat].count(1) / float(node_pop)
        node_perc_pop = float(node_pop)/float(root_size)

        if tree_in_list[node_ind][5] == 'NT':
                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Further Split using var %d at %.1f)" % (tree_in_list[node_ind][1], tree_in_list[node_ind][2], tree_in_list[node_ind][0], node_pop, node_perc_pop, node_prop1, tree_in_list[node_ind][3], tree_in_list[node_ind][4]))
        elif tree_in_list[node_ind][5] == 'T':
                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Terminal Node)" % (tree_in_list[node_ind][1], tree_in_list[node_ind][2], tree_in_list[node_ind][0], node_pop, node_perc_pop, node_prop1))

        temp_str1 = "Node: %d (%s)\\n Size: %d, Perc Pop: %.3f \\n PercFailure: %.3f" % (tree_in_list[node_ind][1], tree_in_list[node_ind][2], node_pop, node_perc_pop, node_prop1)
        temp_node = pydot.Node(temp_str1)  
        plot_node_list.append([tree_in_list[node_ind][1], temp_node])
    else:
        print("Node %d (%s), Parent %d, Size: %d, PercPop: NA, PercFailure:  NA (Terminal Node)" % (tree_in_list[node_ind][1], tree_in_list[node_ind][2], tree_in_list[node_ind][0], node_pop))
        temp_str1 = "Node: %d (%s)\\n Size: %d, Perc Pop: NA \\n PercFailure: NA" % (tree_in_list[node_ind][1], tree_in_list[node_ind][2], node_pop)
        temp_node = pydot.Node(temp_str1)  
        plot_node_list.append([tree_in_list[node_ind][1], temp_node])
            

    left_child_node_ind = -1
    right_child_node_ind = -1

    for i in range(len(tree_in_list)):
        if ((tree_in_list[i][0] == tree_in_list[node_ind][1]) & (tree_in_list[i][2] == 'L')):
            left_child_node_ind = i
            break

    for i in range(len(tree_in_list)):
        if ((tree_in_list[i][0] == tree_in_list[node_ind][1]) & (tree_in_list[i][2] == 'R')):
            right_child_node_ind = i
            break            

    if left_child_node_ind != -1:
        left_child, right_child = test_split(tree_in_list[node_ind][3], tree_in_list[node_ind][4], tree_dat, tree_in_list[node_ind][1], 1, 0) 
        populate_tree_from_list(tree_in_list, left_child, left_child_node_ind)

    if right_child_node_ind != -1:
        left_child, right_child = test_split(tree_in_list[node_ind][3], tree_in_list[node_ind][4], tree_dat, tree_in_list[node_ind][1], 0, 0) 
        populate_tree_from_list(tree_in_list, right_child, right_child_node_ind)

    if left_child_node_ind == -1 and right_child_node_ind == -1:
        for row in tree_dat:
                tree_lineage_custom[row[0]] = tree_lineage_custom[row[0]] + str(tree_in_list[node_ind][1]) + "_"
              
                
def custom_split_leaf(split_leaf_nmbr, split_index, split_value, dataset):
        global tree_list_orig
        global tree_list_custom
        global tree_lineage_orig       
                     
        if len(tree_list_custom) == 0:
                tree_list_custom = tree_list_orig.copy()
        else:
                tree_list_orig = tree_list_custom.copy()

        if tree_lineage_custom[0] != "":
                tree_lineage_orig = tree_lineage_custom.copy() 

        max_node_nmbr = -1
        for i in range(len(tree_list_custom)):
                if tree_list_custom[i][1] > max_node_nmbr:
                      max_node_nmbr = tree_list_custom[i][1]
                      
        split_leaf_ind = -1
        for i in range(len(tree_list_custom)):
                if tree_list_custom[i][1] == split_leaf_nmbr:
                        split_leaf_ind = i
                        break
        
        if split_leaf_ind == -1:
                print('Specified Node Does Not Exit')
        elif tree_list_custom[split_leaf_ind][5] == 'NT':
                print('Cannot Split Non-Terminal Node')
        else:
                tree_list_custom[split_leaf_ind][3], tree_list_custom[split_leaf_ind][4], tree_list_custom[split_leaf_ind][5] = split_index, split_value, 'NT'
                row_num = 0
                cust_split_node_dat = list()
                
                for row in dataset:
                      tmp1 = tree_lineage_orig[row_num].split("_")
                      del tmp1[-1]
                      tmp1 = [int(x) for x in tmp1]
                      if split_leaf_nmbr in tmp1:
                             cust_split_node_dat.append(row)
                      row_num = row_num + 1
                      
                left_child, right_child = test_split(split_index, split_value, cust_split_node_dat, split_leaf_nmbr, 0, 0)
                if left_child:
                      temp_left_split = get_split(left_child, max_node_nmbr + 1, 0)
                      tree_list_custom.append([split_leaf_nmbr, max_node_nmbr + 1,'L', -99, -99, 'T', temp_left_split['gini_list']])
                      max_node_nmbr = max_node_nmbr + 1
                if right_child:
                      temp_right_split = get_split(right_child, max_node_nmbr + 1, 0)
                      tree_list_custom.append([split_leaf_nmbr, max_node_nmbr + 1,'R', -99, -99, 'T', temp_left_split['gini_list']])
                
def get_successor_list(rem_node_nmbr):
      global successor_tree
      for i in range(len(tree_list_orig)):
              if tree_list_orig[i][0] == rem_node_nmbr:
                      successor_tree.append(tree_list_orig[i][1])
                      get_successor_list(tree_list_orig[i][1])
                      

def custom_remove_node(rem_node_nmbr):
        global tree_list_orig
        global tree_list_custom
        global successor_tree
                     
        if len(tree_list_custom) == 0:
                tree_list_custom = tree_list_orig.copy()
        else:
                tree_list_orig = tree_list_custom.copy()

        successor_tree = list()
        successor_tree.append(rem_node_nmbr)
        get_successor_list(rem_node_nmbr)

        i = 0
        while i < len(tree_list_custom):
                if tree_list_custom[i][1] in successor_tree:
                        del tree_list_custom[i]
                else:
                        i = i + 1

def custom_edit_node(edit_node_nmbr, edit_index, edit_value):
        global tree_list_orig
        global tree_list_custom
                     
        if len(tree_list_custom) == 0:
                tree_list_custom = tree_list_orig.copy()
        else:
                tree_list_orig = tree_list_custom.copy()


        for i in range(len(tree_list_orig)):
                if tree_list_custom[i][1] == edit_node_nmbr:
                        tree_list_custom[i][3] = edit_index
                        tree_list_custom[i][4] = edit_value

##def show_gini(tree_list_orig, node_nmbr)
                        
def undo():
        global tree_list_orig
        global tree_list_custom
        tree_list_custom = tree_list_orig.copy()
        
    
    

##dataset = df1.values.tolist()
tree = build_tree(dataset, 4, 1)
##print_tree(tree, tree['full_pop'], tree['prop1'])
##print(tree_list_orig)
populate_tree_from_list(tree_list_orig, dataset, 0)
graph = plot_tree(tree_list_orig, plot_node_list, "Tree_V1") 


               
