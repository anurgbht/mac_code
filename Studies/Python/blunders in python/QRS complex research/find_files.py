import os
import pandas as pd


def get_dir(walk_dir):
    original_path = os.getcwd()
    os.chdir(walk_dir)
    temp = pd.DataFrame()
    for root,subdirs,files in os.walk(walk_dir):
        print(root,subdirs,files)
        tt = [root,subdirs,files]
        temp = temp.append([tt])
    print(temp)
    temp.columns = ['root','folders','files']
    write_path =original_path +'/files.csv' 
    temp.to_csv(write_path,index=False)


def call_get_dir():
    walk_path = input('Enter a path\n')
    print(walk_path)
    get_dir(walk_path)

call_get_dir()
