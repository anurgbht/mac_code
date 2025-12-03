import os
import math
import numpy as np
import pandas as pd
import pylab as plt
import random as rd
import pydotplus as pydot
from operator import itemgetter

#########################################################################################################
#########################################################################################################
#########################################################################################################

class Node():
    global mod_dat
    global nx
    global min_size
    global col_names
    global max_depth
    
    def __init__(self,tree,name,parent,index):
        tree.nodes.append(self)
        tree.names.append(name)
        self.name = name
        self.parent = parent
        self.index = index
        self.children = self.__return_split_nodes(tree)

    def __return_split_nodes(self,tree):
        temp_dat = [mod_dat[i] for i in self.index]
        current_target = [x[-1] for x in temp_dat]
        self.zeros = current_target.count(0)
        self.ones = current_target.count(1)
        self.population = self.ones + self.zeros
        self.depth = self.__find_depth(tree)
        
        if ((self.population > min_size) and (self.depth < max_depth)):
            best_split = self.__find_best_split(temp_dat)
            if len(best_split) > 0:
                left_index = [int(x[0]) for x in best_split[0]]
                right_index = [int(x[0]) for x in best_split[1]]
                self.split_var_index = best_split[2]
                self.split_var_value = best_split[3]
                self.gini = best_split[4]
                temp_node_left = Node(tree,max(tree.names) + 1,self.name,left_index)
                temp_node_right = Node(tree,max(tree.names) + 1,self.name,right_index)
                return [temp_node_left,temp_node_right]
            else:
                self.split_var_index = None
                self.split_var_value = None
                self.gini = -.999
                return []
        else:
            self.split_var_index = None
            self.split_var_value = None
            self.gini = -.999
            return []

    def __find_depth(self,tree):
        tt = 0
        for node in tree.nodes:
            if self.parent != None:
                if self.parent == node.name:
                    tt += 1
                    tt += node.depth
            else:
                break
        return tt
    
    def __find_best_split(self,temp_dat):
        max_gini = 0
        best_split = []
        for i in range(nx):
            split_dat_index = [0,i+1,-1]
            split_x_dat = [[x[i] for i in split_dat_index] for x in temp_dat]
            split_x_dat = sorted(split_x_dat, key=itemgetter(1))
            # alternate way to sort the split_x_dat
            # split_x_dat.sort(key=lambda x: x[1])
            for j in range(len(temp_dat)-   1):
                left = split_x_dat[:j+1]
                right = split_x_dat[j+1:]
                temp_gini = self.__gini_index(left,right,[0,1],split_x_dat)
                if temp_gini > max_gini:
                    max_gini = temp_gini
                    best_split = [left,right,col_names[i],right[0][1],temp_gini]
        return best_split

    def __gini_index(self,left,right,class_values,split_dat):
        gini1 = 0.0
        gini2 = 0.0
        gini3 = 0.0
        gini_node_cmpl = 0.0
        sizeL = len(left)
        sizeR = len(right)
         
        for class_value in class_values:
            gini_node_cmpl += math.pow([row[-1] for row in split_dat].count(class_value) / float(len(split_dat)),2)                        
            if sizeL == 0:
                proportionL = 0
            else:
                proportionL = [row[-1] for row in left].count(class_value) / float(sizeL)

            if sizeR == 0:
                proportionR = 0
            else:
                proportionR = [row[-1] for row in right].count(class_value) / float(sizeR)
                    
            gini1 += (proportionL * (1.0 - proportionL)) + (proportionR * (1.0 - proportionR))
            gini2 += math.pow(proportionL,2) * (sizeL/(sizeL + sizeR)) + math.pow(proportionR,2) * (sizeR/(sizeL + sizeR)) 

        gini3 = 1 - gini_node_cmpl - (sizeL/(sizeL + sizeR)) - (sizeR/(sizeL + sizeR)) + gini2 
        return gini3


class Tree():
    global mod_dat
    global col_names
    def __init__(self):
        self.nodes = []
        self.names = []
        
    def build_tree(self):
        temp_node = Node(self,0,None,[int(x[0]) for x in mod_dat])

    def print_tree(self):
        print("\n--------------------------------------------------------------------------------")
        print("Printing Tree information now.")
        print("--------------------------------------------------------------------------------")
        for node in self.nodes:
            print('Name : {0}, Parent : {1}, Split Variable : {2}, Split Value = {3}, Gini = {4:.3f}, Population : {6}, Ones : {7}, Zeros : {8}'
                  .format(node.name,node.parent,node.split_var_index,node.split_var_value,node.gini,node.index,node.population,node.ones,node.zeros))

    def plot_tree(self):
        graph = pydot.Dot(graph_type='graph')
        for parent_node in self.nodes:
            # if i see each node as parent, i need to find its children
            for child_node in self.nodes:
                if parent_node.name == child_node.parent:
                    # less than is always on the left
                    p = self.__make_text(parent_node)
                    c = self.__make_text(child_node)
                    graph.add_edge(pydot.Edge(p,c))
        graph.write_png('my_tree.png')

    def __make_text(self,node):
        if node.gini > 0:
            tt = 'Name : {0}, Parent : {1}, \nSplit at {2}<={3}, Gini = {4:.3f}, \nPopulation : {6}, Ones : {7}, Zeros : {8}'.format(node.name,node.parent,node.split_var_index,node.split_var_value,node.gini,node.index,node.population,node.ones,node.zeros)
            if node.parent == None:
                tt = 'Name : {0},\nSplit at {2}<={3}, Gini = {4:.3f}, \nPopulation : {6}, Ones : {7}, Zeros : {8}'.format(node.name,node.parent,node.split_var_index,node.split_var_value,node.gini,node.index,node.population,node.ones,node.zeros)
        else:
            tt = 'Name : {0}, Parent : {1}, \nPopulation : {6}, Ones : {7}, Zeros : {8}'.format(node.name,node.parent,node.split_var_index,node.split_var_value,node.gini,node.index,node.population,node.ones,node.zeros)
        return tt
        

    
#########################################################################################################
#########################################################################################################
#########################################################################################################

# 0 is index, -1 is y. Xs are in between. nx to be specified
global mod_dat
global nx
global max_depth
global col_names
global min_size
global max_depth

mod_excel = pd.read_excel("DT_data.xlsx",sheet_name = "mod_data")
mod_excel = mod_excel.dropna().reset_index().drop('index',1)
nx = mod_excel.shape[1]-2
mod_dat = [list(x) for x in mod_excel.values]
col_names = mod_excel.columns[1:-1]
print(col_names)
min_size = int(mod_excel.shape[0]/10)
max_depth = 10

tree = Tree()
tree.build_tree()
##tree.print_tree()
tree.plot_tree()

#########################################################################################################
#########################################################################################################
#########################################################################################################
