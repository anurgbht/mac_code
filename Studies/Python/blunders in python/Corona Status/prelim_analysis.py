import re
import os
import sys
import requests
import urllib.request
import pandas as pd
import pylab as plt
from tabula import read_pdf
from bs4 import BeautifulSoup

##sys.path.append('C:\\Program Files\\Java\\jre1.8.0_241\\bin')

#################################################################################
#################################################################################
#################################################################################

def get_soup(l):
    page = urllib.request.urlopen(l)
    return BeautifulSoup(page)

def get_groups(parent):
    
    soup = get_soup(parent)

    sub_groups = soup.find('div',{'id':"PageContent_C006_Col01"}).find_all('a')

    tt = []

    for i,l in enumerate(sub_groups):
        sl = l.get('href')
        if sl != parent:
            tt.append(sl)

    return tt

def find_regions(row):
    interested = ['China','Germany','India','Spain','France']
    if row.region in interested:
        return 1
    else:
        return 0

#################################################################################
#################################################################################
#################################################################################

## extracting the relevant links
## not included the  "more" sections in each page
parent_link = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports'
who_home = 'https://www.who.int'

pdf_links = get_groups(parent_link)

write_path = os.getcwd() + '/sit-rep/'

col_names = ['region','cases','new_cases','deaths','new_deaths','transmission','days']

for pdf_link in pdf_links:
    tt = requests.get(who_home+pdf_links[0])
    fname = pdf_link.split('/')[-1].split('?')[0]
    print(fname)
    if 'covid' in fname:
        with open(write_path+fname,'wb') as f:
            f.write(tt.content)
    else:
        print('skipped parsing')

    temp_df = pd.DataFrame(columns = col_names)
    
    dfs = read_pdf(write_path+fname,pages='all')
    print(len(dfs))
    for df in dfs:
        if df.shape[1] == 7:
            df.columns = col_names
            temp_df = pd.concat([temp_df,df])
            print(temp_df.shape)
    temp_df = temp_df.dropna().reset_index(drop=1)
    temp_df.loc[:,'interested'] = temp_df.apply(find_regions,1)
    subset_df = temp_df.loc[temp_df.loc[:,'interested'] == 1,:].reset_index(drop=1)
    plt.bar(subset_df.region,[float(x) for x in subset_df.cases])
    plt.show()
    break
