
##python -m pip install matplotlib (run the code on the left to install matplotlib from cmd D:)
##python -m pip install --index-url=http://pypi.python.org/pypi/ --trusted-host pypi.python.org pydot

import pandas as pandas
import pydotplus as pydot
import datetime
import math
import os

pandas.set_option('display.max_rows', 8000)
pandas.set_option('display.precision', 2)

start_time = datetime.datetime.now()
print(("Start Date & Time: %s-%s-%s %s:%s:%s")%(start_time.day, start_time.month, start_time.year, start_time.hour, start_time.minute, start_time.second)) 

FeatureDat_DT = pandas.read_excel('DT_data.xlsx',sheet_name = 'dummy_data', header=0, sep=',', parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
##FeatureDat_DT = pandas.read_csv("FeatureDat_DT_V4.csv", header=0, sep=',', parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)
df2 = FeatureDat_DT.fillna(-99999)
##df2 = df2[['STAVES_RIB_TEMP_B1_TWO_std_last7days','target']]
dataset = df2.values.tolist()

##dataset = [[0,20,12,1],
##[0,0,30,1],
##[-99999,15,20,1],
##[-99999,5,5,0],
##[3,6,12,0],
##[4,3,13,0],
##[5,9,4,0],
##[6,4,6,0],
##[20,0,2,0]]

q = 0
for row in dataset:
        row.insert(0,q)
        q = q + 1

##col_list = ['Index','Var1','Var2','Var3','Target']

node_cntr = 0
graph = pydot.Dot(graph_type='digraph')
tree_list = list()
split_dat = list()
alt_split_dat = list()
left, right = list(), list()
left_right = list()
successor_tree = list()
plot_node_list = list()
tree_lineage = {}
num_alt_splits = 200 # specify number of alternate splits
tuyer_tree_name = "Tree_TuyerFailure_VM_4_Depth_X"

col_list = list()
col_list.append('row_num')
for col in df2:
        col_list.append(col)

root_size = len(dataset)


# Split a dataset based on an attribute and an attribute value
def test_split(index, value, node_cntr, add_lineage_ind, min_size):
##        global tree_lineage
        global split_dat
        global left
        global right
        left, right = list(), list()
        
##        for row in split_dat:
##                if add_lineage_ind == 1:
##                                tree_lineage[row[0]].append(node_cntr)
##                                        
##                if row[index] <= value:
##                        left.append(row)                                                                                
##                else:
##                        right.append(row)

        left = [x for x in split_dat if x[index] <= value]
        right = [x for x in split_dat if x[index] > value]

        min_size_breach = 0
        if (len(left) < min_size) or (len(right) < min_size):
                min_size_breach = 1
                
        return min_size_breach
 
# Calculate the Gini index for a split dataset
def gini_index(class_values):
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


# Recreate the parent dataset for the given node
def recreate_split_dat(node_cntr):
        global split_dat

##        split_dat = list()
##        for row in dataset:
##                if node_cntr in tree_lineage[row[0]]:
##                        split_dat.append(row)

        split_dat = [dataset[x] for x in tree_lineage[node_cntr]]

        return


# Select the best split point for a dataset
def get_split(node_cntr, min_size):
        global left
        global right

        recreate_split_dat(node_cntr)
        
        full_pop = len(split_dat)

        prop1 = [row[-1] for row in split_dat].count(1) / float(full_pop)
        perc_pop = float(full_pop)/float(root_size)
        alt_splits = list()        
        class_values = list(set(row[-1] for row in split_dat))
        split_dat_trnspse = [list(i) for i in zip(*split_dat)]
        b_index, b_value, b_score = None, None, None
        
        for index in range(1, len(split_dat[0])-1):
                print(index)
                col_index_unique_vals = set([round(x,1) for x in split_dat_trnspse[index]])
                for q in col_index_unique_vals:
                        size_breach = test_split(index, q, node_cntr, 0, min_size)
                        if size_breach == 0:
                                gini = gini_index(class_values)
                                alt_splits.append([index, q, gini])
                                if (b_score == None) or (gini > b_score):
                                        b_index, b_value, b_score = index, q, gini
 
        if len(alt_splits) > 0:
                size_breach = test_split(b_index, b_value, node_cntr, 0, min_size)
                t1 = sorted(alt_splits, key=lambda x: x[2], reverse=True)
                col_index_arr = list()
                t2 = []
                for i in range(len(t1)):
                        if t1[i][0] not in col_index_arr:
                                t2.append(t1[i])
                                col_index_arr.append(t1[i][0])
                        
                t4 = t2[:num_alt_splits] 
                left_size = len(left)
                right_size = len(right)
                
                if left_size ==0:
                        left_prop1 = -99999
                else:
                        left_prop1 = [row[-1] for row in left].count(1) / float(left_size)

                if right_size ==0:
                        right_prop1 = -99999
                else:
                        right_prop1 = [row[-1] for row in right].count(1) / float(right_size)
                    
                return {'full_pop':full_pop, 'prop1':prop1, 'perc_pop':perc_pop, 'index':b_index, 'col_name':col_list[b_index], 'value':b_value, 'alt_splits':t4, 'left_size':left_size, 'left_prop1':left_prop1, 'right_size':right_size, 'right_prop1':right_prop1}
        else:
                left, right = list(), list()
                print("No Split available based on minimum size criterion.")
                return {'full_pop':full_pop, 'prop1':prop1, 'perc_pop':perc_pop, 'index':b_index, 'col_name':'NA', 'value':b_value, 'alt_splits':[], 'left_size':999, 'left_prop1':999, 'right_size':999, 'right_prop1':999}

# Generate list of alternate splits
def get_alt_splits(min_size, node_cntr):
        node_alt_splits = list()
        recreate_split_dat(node_cntr)
        
        if len(split_dat) > 0:
                class_values = list(set(row[-1] for row in split_dat))
                split_dat_trnspse = [list(i) for i in zip(*split_dat)]
                for index in range(1, len(split_dat[0])-1):
                        print(index)
                        col_index_unique_vals = set([round(x,1) for x in split_dat_trnspse[index]])
                        for q in col_index_unique_vals:
                                size_breach = test_split(index, q, -99, 0, min_size)
                                if size_breach == 0:
                                        gini = gini_index(class_values)
                                        node_alt_splits.append([index, q, gini])
                                
                c1 = sorted(node_alt_splits, key=lambda x: x[2], reverse=True)
                col_index_arr = list()
                c2 = []
                for i in range(len(c1)):
                        if c1[i][0] not in col_index_arr:
                                c2.append(c1[i])
                                col_index_arr.append(c1[i][0])
                                
                c4 = c2[:num_alt_splits]
        else:
                c4 = node_alt_splits
                
        return c4
 



# Create child splits for a node or make terminal
def split(max_depth, min_size, depth, parent_node):
##        global left
##        global right
        global node_cntr
        global tree_list
        global tree_lineage
        global plot_node_list
##        global split_dat
        
        # check for split which does not meet minimum size criterion
        if not left and not right:
                print(("No Split for node %d that meets minimum size criterion")%(parent_node))
                for i in range(len(tree_list)):
                        if tree_list[i][1] == parent_node:
                                tree_list[i][5] = 'T'
                return

        # check for something that should not happen
        if not left or not right:
                print(("Unknown Deformity for node %d")%(parent_node))
                for i in range(len(tree_list)):
                        if tree_list[i][1] == node_cntr:
                                tree_list[i][5] = 'T'
                return
            
        # check for max depth
        if depth >= max_depth:
                # create left & right nodes - and properties
                node_cntr = node_cntr + 1
                left_node_cntr = node_cntr
                tree_lineage[node_cntr] = [row[0] for row in left]

                node_cntr = node_cntr + 1
                tree_lineage[node_cntr] = [row[0] for row in right]

                left_size = len(left)
                left_prop1 = [row[-1] for row in left].count(1) / float(len(left))
                left_perc_pop = float(len(left))/float(root_size)

                right_size = len(right)
                right_prop1 = [row[-1] for row in right].count(1) / float(len(right))
                right_perc_pop = float(len(right))/float(root_size)
                
                # update left node - tree_list, plot_node_list
                alt_splits = get_alt_splits(min_size, left_node_cntr)
                tree_list.append([parent_node,left_node_cntr,'L',-99,-99,'T', alt_splits])

                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (left_node_cntr, 'L', left_size, left_perc_pop, left_prop1))
                plot_node_list.append([left_node_cntr, temp_node])

                # update right node - tree_list, plot_node_list
                alt_splits = get_alt_splits(min_size, node_cntr)
                tree_list.append([parent_node,node_cntr,'R',-99,-99,'T', alt_splits])

                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (node_cntr, 'R', right_size, right_perc_pop, right_prop1))
                plot_node_list.append([node_cntr, temp_node])
                
                return


        if left and right:
                # process left child
                node_cntr = node_cntr + 1
                tree_lineage[node_cntr] = [row[0] for row in left]

                node = get_split(node_cntr, min_size)
                tree_list.append([parent_node,node_cntr,'L',node['index'], node['value'], 'NT', node['alt_splits']])
                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (node_cntr, 'L', node['full_pop'], node['perc_pop'], node['prop1']))
                plot_node_list.append([node_cntr, temp_node])
                split(max_depth, min_size, depth+1, node_cntr)

                # re-create lost right child (hopefully left never gets lost due to its locational advantage)
                node = get_split(parent_node, min_size)
                        
                # process right child
                node_cntr = node_cntr + 1
                tree_lineage[node_cntr] = [row[0] for row in right]

                node = get_split(node_cntr, min_size)
                tree_list.append([parent_node,node_cntr,'R',node['index'], node['value'], 'NT', node['alt_splits']])
                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (node_cntr, 'R', node['full_pop'], node['perc_pop'], node['prop1']))
                plot_node_list.append([node_cntr, temp_node])
                split(max_depth, min_size, depth+1, node_cntr)

        return
 
# Plot Tree
def plot_tree(tree_name):
        global graph
        graph = pydot.Dot(graph_type='digraph', ratio=0.5)
##        graph.set_size('3,5')

        for i in range(len(plot_node_list)):
                graph.add_node(plot_node_list[i][1])
                
        for i in range(len(tree_list)):
                from_node = tree_list[i][0]
                to_node = tree_list[i][1]

                split_var = -1
                split_val = -1
                for z in range(len(tree_list)):
                        if tree_list[z][1] == from_node:
                                split_var = tree_list[z][3]
                                split_val = tree_list[z][4]
                                
                
                temp1 = -1
                temp2 = -1
                for j in range(len(plot_node_list)):
                        if plot_node_list[j][0] == from_node and from_node > 0:
                                temp1 = j
                        if plot_node_list[j][0] == to_node:
                                temp2 = j
                if temp1 >= 0 and temp2 >= 0:
                        if tree_list[i][2] == 'L':
                                graph.add_edge(pydot.Edge(plot_node_list[temp1][1], plot_node_list[temp2][1], label = '%s <= %.3f' % (col_list[split_var], split_val)))
                        if tree_list[i][2] == 'R':
                                graph.add_edge(pydot.Edge(plot_node_list[temp1][1], plot_node_list[temp2][1], label = '%s > %.3f' % (col_list[split_var], split_val)))
        graph.write_png(tree_name + '.png')

        return
 
def populate_tree_from_list(node_ind):
        global tree_lineage
        global plot_node_list

        recreate_split_dat(tree_list[node_ind][1])
        node_pop = len(split_dat)
        if node_pop > 0:
                node_prop1 = [row[-1] for row in split_dat].count(1) / float(node_pop)
                node_perc_pop = float(node_pop)/float(root_size)

                ##        if tree_list[node_ind][5] == 'NT':
                ##                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Further Split using var %d at %.1f)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop, node_perc_pop, node_prop1, tree_list[node_ind][3], tree_list[node_ind][4]))
                ##        elif tree_list[node_ind][5] == 'T':
                ##                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Terminal Node)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop, node_perc_pop, node_prop1))

                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (tree_list[node_ind][1], tree_list[node_ind][2], node_pop, node_perc_pop, node_prop1))
                plot_node_list.append([tree_list[node_ind][1], temp_node])
        else:
        ##        print("Node %d (%s), Parent %d, Size: %d, PercPop: NA, PercFailure:  NA (Terminal Node)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop))
                temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop NA \\n PercFailure NA" % (tree_list[node_ind][1], tree_list[node_ind][2], node_pop))
                plot_node_list.append([tree_list[node_ind][1], temp_node])
            

        left_child_node_ind = -1
        right_child_node_ind = -1

        for i in range(len(tree_list)):
                if ((tree_list[i][0] == tree_list[node_ind][1]) & (tree_list[i][2] == 'L')):
                        left_child_node_ind = i
                        break

        for i in range(len(tree_list)):
                if ((tree_list[i][0] == tree_list[node_ind][1]) & (tree_list[i][2] == 'R')):
                        right_child_node_ind = i
                        break            

        if left_child_node_ind != -1:
                left_child, right_child = test_split(tree_list[node_ind][3], tree_list[node_ind][4], tree_dat, tree_list[node_ind][1], 1) 
                populate_tree_from_list(left_child, left_child_node_ind)

        if right_child_node_ind != -1:
                left_child, right_child = test_split(tree_list[node_ind][3], tree_list[node_ind][4], tree_dat, tree_list[node_ind][1], 0) 
                populate_tree_from_list(right_child, right_child_node_ind)

        return
        

   
              

def custom_split_leaf(split_leaf_nmbr, split_var, split_value):
        global tree_list
        global tree_lineage
        global plot_node_list
                     
        split_index = -1
        for i in range(len(col_list)):
                if col_list[i] == split_var:
                        split_index = i
               
        max_node_nmbr = -1
        for i in range(len(tree_list)):
                if tree_list[i][1] > max_node_nmbr:
                      max_node_nmbr = tree_list[i][1]
        
        split_leaf_ind = -1
        for i in range(len(tree_list)):
                if tree_list[i][1] == split_leaf_nmbr:
                        split_leaf_ind = i
                        break
        
        if split_leaf_ind == -1:
                print('Specified Node Does Not Exist')
        elif tree_list[split_leaf_ind][5] == 'NT':
                print('Cannot Split Non-Terminal Node')
        elif split_index == -1:
                print('Could Not Find Specified Split Variable in Data')
        else:
                tree_list[split_leaf_ind][3], tree_list[split_leaf_ind][4], tree_list[split_leaf_ind][5] = split_index, split_value, 'NT'
                recreate_split_dat(split_leaf_nmbr)
                size_breach = test_split(split_index, split_value, split_leaf_nmbr, 0, 10)

                if not left or not right:
                        print("Cannot split further! Sorry!")
                        return
                else:
                        tree_lineage[max_node_nmbr+1] = [row[0] for row in left]
                        tree_lineage[max_node_nmbr+2] = [row[0] for row in right]
                        
                        node = get_split(max_node_nmbr+1,1)
                        tree_list.append([split_leaf_nmbr,max_node_nmbr+1,'L',-99, -99, 'T', node['alt_splits']])
                        temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (max_node_nmbr+1, 'L', node['full_pop'], node['perc_pop'], node['prop1']))
                        plot_node_list.append([max_node_nmbr+1, temp_node])
                        
                        node = get_split(max_node_nmbr+2,1)
                        tree_list.append([split_leaf_nmbr,max_node_nmbr+2,'R',-99, -99, 'T', node['alt_splits']])
                        temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (max_node_nmbr+2, 'R', node['full_pop'], node['perc_pop'], node['prop1']))
                        plot_node_list.append([max_node_nmbr+2, temp_node])
                
        plot_tree(tuyer_tree_name + "_cust")
        
        return
                
def get_successor_list(rem_node_nmbr):
        global successor_tree
        for i in range(len(tree_list)):
              if tree_list[i][0] == rem_node_nmbr:
                      successor_tree.append(tree_list[i][1])
                      get_successor_list(tree_list[i][1])

        return
      
def custom_remove_node_successors(rem_node_nmbr):
        global tree_list
        global tree_lineage
        global successor_tree
        global plot_node_list

        for i in range(len(tree_list)):
                if tree_list[i][1] == rem_node_nmbr:
                        tree_list[i][5] = 'T'
        
        successor_tree = list()
        get_successor_list(rem_node_nmbr)

        i = 0
        while i < len(tree_list):
                if tree_list[i][1] in successor_tree:
                        tree_lineage[tree_list[i][1]] = []
                        del tree_list[i]
                else:
                        i = i + 1

        i = 0
        while i < len(plot_node_list):
                if plot_node_list[i][0] in successor_tree:
                        del plot_node_list[i]
                else:
                        i = i + 1

        plot_tree(tuyer_tree_name + "_cust")

        return
                

def refresh_alt_splits_tables(edit_node_nmbr):
        global tree_list
        global successor_tree

        successor_tree = list()
        get_successor_list(edit_node_nmbr)

        for i in range(len(tree_list)):
                if tree_list[i][1] in successor_tree:
                        row_num = 0
                        curr_node_dat = list()
                        for row in dataset:
                                tmp1 = tree_lineage[row_num].split("_")
                                del tmp1[-1]
                                tmp1 = [int(x) for x in tmp1]
                                if tree_list[i][1] in tmp1:
                                        curr_node_dat.append(row)
                                row_num = row_num + 1

                        alt_splits = get_alt_splits(curr_node_dat)
                        tree_list[i][6] = alt_splits

        return

def custom_edit_node(edit_node_nmbr, edit_var, edit_value):
        global tree_list
        global tree_lineage
        global plot_node_list  
        
        edit_col_index = -1
        for i in range(len(col_list)):
                if col_list[i] == edit_var:
                        edit_col_index = i

        if edit_col_index == -1:
                print('Could Not Find Specified Split Variable in Data')
        else:
                for i in range(len(tree_list)):
                        if tree_list[i][1] == edit_node_nmbr:
                                tree_list[i][3] = edit_col_index
                                tree_list[i][4] = edit_value

        refresh_alt_splits_tables(edit_node_nmbr)
        plot_tree(tuyer_tree_name + "_cust")

        return

def show_alternate_splits(node_nmbr):
        for i in range(len(tree_list)):
                if tree_list[i][1] == node_nmbr:
                        df_gini = pandas.DataFrame(tree_list[i][6])
                        df_gini.columns = ['SplitVar_Col_Index', 'Split_Value','Gini']
                        df_gini['Split_Variable'] = [col_list[x] for x in df_gini['SplitVar_Col_Index']]
                        df_gini = df_gini.drop('SplitVar_Col_Index', 1)
                        df_gini_cols = df_gini.columns.tolist()
                        df_gini_cols = df_gini_cols[-1:] + df_gini_cols[:-1]
                        df_gini = df_gini[df_gini_cols]
                        break
        print(df_gini)
 


# Build a decision tree - Main Function
def build_tree(max_depth, min_size):
        global node_cntr
        global split_dat
        global tree_lineage

        split_dat = dataset
        end_time = datetime.datetime.now()
        print(("End Date & Time: %s-%s-%s %s:%s:%s")%(end_time.day, end_time.month, end_time.year, end_time.hour, end_time.minute, end_time.second))
        node_cntr = node_cntr + 1
        tree_lineage[node_cntr] = [row[0] for row in split_dat]
        end_time = datetime.datetime.now()
        print(("Start Date & Time: %s-%s-%s %s:%s:%s")%(end_time.day, end_time.month, end_time.year, end_time.hour, end_time.minute, end_time.second))
        root = get_split(node_cntr, min_size)
        end_time = datetime.datetime.now()
        print(("End Date & Time: %s-%s-%s %s:%s:%s")%(end_time.day, end_time.month, end_time.year, end_time.hour, end_time.minute, end_time.second))
        temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (node_cntr, 'P', root['full_pop'], root['perc_pop'], root['prop1']))
        plot_node_list.append([node_cntr, temp_node])
        end_time = datetime.datetime.now()
        print(("End Date & Time: %s-%s-%s %s:%s:%s")%(end_time.day, end_time.month, end_time.year, end_time.hour, end_time.minute, end_time.second))
        if max_depth > 0:
                tree_list.append([0,node_cntr,'P',root['index'], root['value'], 'NT', root['alt_splits']])
                split(max_depth, min_size, 1, node_cntr)
        else:
                tree_list.append([0,node_cntr,'P',-99, -99, 'T', root['alt_splits']])
##        populate_tree_from_list(dataset, 0)
        plot_tree(tuyer_tree_name)

        return root

tree = build_tree(0, 10)

end_time = datetime.datetime.now()
print(("End Date & Time: %s-%s-%s %s:%s:%s")%(end_time.day, end_time.month, end_time.year, end_time.hour, end_time.minute, end_time.second))
print(("Time Taken %s")%(end_time - start_time))

##############################################################################################################################################################



##
##    
## 
### Create a terminal node value
####def to_terminal():
####        outcomes = [row[-1] for row in left_right]
####        return max(set(outcomes), key=outcomes.count)
## 
##
### Print a decision tree
##def print_tree(node, size, prop1, depth=0):
##        if isinstance(node, dict):
##                print('%s[X%d (%s) <= %.3f], Size: %d, Perc of Root Pop: %.3f, Prop1: %.3f' % (depth*' ', (node['index']+1), node['col_name'], node['value'], node['full_pop'], node['perc_pop'], node['prop1']))
##                print(pandas.DataFrame(node['alt_splits']))
##                print_tree(node['left'], node['left_size'], node['left_prop1'], depth+1)
##                print_tree(node['right'], node['right_size'], node['right_prop1'], depth+1)
##        else:
##                print('%s[%d], Size: %d, Perc of Root Pop: %.3f, Prop1: %.3f' % ((depth*' ', node, size, size/root_size, prop1)))
##
##
##
##
##
##def populate_tree_from_list(tree_dat, node_ind):
##    global tree_lineage
##    global plot_node_list
##    
##    node_pop = len(tree_dat)
##    if node_pop > 0:
##        node_prop1 = [row[-1] for row in tree_dat].count(1) / float(node_pop)
##        node_perc_pop = float(node_pop)/float(root_size)
##
##        if tree_list[node_ind][5] == 'NT':
##                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Further Split using var %d at %.1f)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop, node_perc_pop, node_prop1, tree_list[node_ind][3], tree_list[node_ind][4]))
##        elif tree_list[node_ind][5] == 'T':
##                print("Node %d (%s), Parent %d, Size: %d, PercPop: %.3f, PercFailure:  %.3f (Terminal Node)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop, node_perc_pop, node_prop1))
##
##        temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop %.3f \\n PercFailure %.3f" % (tree_list[node_ind][1], tree_list[node_ind][2], node_pop, node_perc_pop, node_prop1))
##        plot_node_list.append([tree_list[node_ind][1], temp_node])
##    else:
##        print("Node %d (%s), Parent %d, Size: %d, PercPop: NA, PercFailure:  NA (Terminal Node)" % (tree_list[node_ind][1], tree_list[node_ind][2], tree_list[node_ind][0], node_pop))
##        temp_node = pydot.Node("Node %d (%s) \\n Size %d, Perc Pop NA \\n PercFailure NA" % (tree_list[node_ind][1], tree_list[node_ind][2], node_pop))
##        plot_node_list.append([tree_list[node_ind][1], temp_node])
##            
##
##    left_child_node_ind = -1
##    right_child_node_ind = -1
##
##    for i in range(len(tree_list)):
##        if ((tree_list[i][0] == tree_list[node_ind][1]) & (tree_list[i][2] == 'L')):
##            left_child_node_ind = i
##            break
##
##    for i in range(len(tree_list)):
##        if ((tree_list[i][0] == tree_list[node_ind][1]) & (tree_list[i][2] == 'R')):
##            right_child_node_ind = i
##            break            
##
##    if left_child_node_ind != -1:
##        left_child, right_child = test_split(tree_list[node_ind][3], tree_list[node_ind][4], tree_dat, tree_list[node_ind][1], 1) 
##        populate_tree_from_list(left_child, left_child_node_ind)
##
##    if right_child_node_ind != -1:
##        left_child, right_child = test_split(tree_list[node_ind][3], tree_list[node_ind][4], tree_dat, tree_list[node_ind][1], 0) 
##        populate_tree_from_list(right_child, right_child_node_ind)
##
##    if left_child_node_ind == -1 and right_child_node_ind == -1:
##        for row in tree_dat:
##                tree_lineage[row[0]] = tree_lineage[row[0]] + str(tree_list[node_ind][1]) + "_"
##   
##              
##
##def custom_split_leaf(split_leaf_nmbr, split_var, split_value):
##        global tree_list
##        global tree_lineage
##        global plot_node_list
##        global cust_split_node_dat
##                     
##        split_index = -1
##        for i in range(len(col_list)):
##                if col_list[i] == split_var:
##                        split_index = i
##               
##        max_node_nmbr = -1
##        for i in range(len(tree_list)):
##                if tree_list[i][1] > max_node_nmbr:
##                      max_node_nmbr = tree_list[i][1]
##        
##        split_leaf_ind = -1
##        for i in range(len(tree_list)):
##                if tree_list[i][1] == split_leaf_nmbr:
##                        split_leaf_ind = i
##                        break
##        
##        if split_leaf_ind == -1:
##                print('Specified Node Does Not Exist')
##        elif tree_list[split_leaf_ind][5] == 'NT':
##                print('Cannot Split Non-Terminal Node')
##        elif split_index == -1:
##                print('Could Not Find Specified Split Variable in Data')
##        else:
##                tree_list[split_leaf_ind][3], tree_list[split_leaf_ind][4], tree_list[split_leaf_ind][5] = split_index, split_value, 'NT'
##                row_num = 0
##                cust_split_node_dat = list()
##                
##                for row in dataset:
##                      tmp1 = tree_lineage[row_num].split("_")
##                      del tmp1[-1]
##                      tmp1 = [int(x) for x in tmp1]
##                      if split_leaf_nmbr in tmp1:
##                             cust_split_node_dat.append(row)
##                      row_num = row_num + 1
##     
##                left_child, right_child = test_split(split_index, split_value, cust_split_node_dat, split_leaf_nmbr, 0)
##                temp_alt_splits = get_alt_splits(left_child)
##                tree_list.append([split_leaf_nmbr, max_node_nmbr + 1,'L', -99, -99, 'T', temp_alt_splits])
##                max_node_nmbr = max_node_nmbr + 1
##                temp_alt_splits = get_alt_splits(right_child)
##                tree_list.append([split_leaf_nmbr, max_node_nmbr + 1,'R', -99, -99, 'T', temp_alt_splits])
##
##        plot_node_list = list()
##        tree_lineage = [""]*len(dataset)
##        populate_tree_from_list(dataset, 0)
##        plot_tree("Tree_V0")
##                
##def get_successor_list(rem_node_nmbr):
##      global successor_tree
##      for i in range(len(tree_list)):
##              if tree_list[i][0] == rem_node_nmbr:
##                      successor_tree.append(tree_list[i][1])
##                      get_successor_list(tree_list[i][1])
##                      
##
##def custom_remove_node_successors(rem_node_nmbr):
##        global tree_list
##        global tree_lineage
##        global successor_tree
##        global plot_node_list
##
##        for i in range(len(tree_list)):
##                if tree_list[i][1] == rem_node_nmbr:
##                        tree_list[i][5] = 'T'
##        
##        successor_tree = list()
##        get_successor_list(rem_node_nmbr)
##
##        i = 0
##        while i < len(tree_list):
##                if tree_list[i][1] in successor_tree:
##                        del tree_list[i]
##                else:
##                        i = i + 1
##
##        plot_node_list = list()
##        tree_lineage = [""]*len(dataset)
##        populate_tree_from_list(dataset, 0)
##        plot_tree("Tree_V0")        
##
##def refresh_alt_splits_tables(edit_node_nmbr):
##        global tree_list
##        global successor_tree
##
##        successor_tree = list()
##        get_successor_list(edit_node_nmbr)
##
##        for i in range(len(tree_list)):
##                if tree_list[i][1] in successor_tree:
##                        row_num = 0
##                        curr_node_dat = list()
##                        for row in dataset:
##                                tmp1 = tree_lineage[row_num].split("_")
##                                del tmp1[-1]
##                                tmp1 = [int(x) for x in tmp1]
##                                if tree_list[i][1] in tmp1:
##                                        curr_node_dat.append(row)
##                                row_num = row_num + 1
##
##                        alt_splits = get_alt_splits(curr_node_dat)
##                        tree_list[i][6] = alt_splits
##
##
##def custom_edit_node(edit_node_nmbr, edit_var, edit_value):
##        global tree_list
##        global tree_lineage
##        global plot_node_list  
##        
##        edit_index = -1
##        for i in range(len(col_list)):
##                if col_list[i] == edit_var:
##                        edit_index = i
##
##        if edit_index == -1:
##                print('Could Not Find Specified Split Variable in Data')
##        else:
##                for i in range(len(tree_list)):
##                        if tree_list[i][1] == edit_node_nmbr:
##                                tree_list[i][3] = edit_index
##                                tree_list[i][4] = edit_value
##
##        plot_node_list = list()
##        tree_lineage = [""]*len(dataset)
##        populate_tree_from_list(dataset, 0)
##        refresh_alt_splits_tables(edit_node_nmbr)
##        plot_tree("Tree_V0")        
##
##def show_alternate_splits(node_nmbr):
##        for i in range(len(tree_list)):
##                if tree_list[i][1] == node_nmbr:
##                        df_gini = pandas.DataFrame(tree_list[i][6])
##                        df_gini.columns = ['SplitVar_Col_Index', 'Split_Value','Gini']
##                        df_gini['Split_Variable'] = [col_list[x] for x in df_gini['SplitVar_Col_Index']]
##                        df_gini = df_gini.drop('SplitVar_Col_Index', 1)
##                        df_gini_cols = df_gini.columns.tolist()
##                        df_gini_cols = df_gini_cols[-1:] + df_gini_cols[:-1]
##                        df_gini = df_gini[df_gini_cols]
##                        break
##        print(df_gini)
##                              
        

 


               
