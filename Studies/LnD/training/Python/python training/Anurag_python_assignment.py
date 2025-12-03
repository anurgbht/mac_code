1) Python code to find address from district and Nikay columns

rdf=pd.read_csv('D:/Bhatt/2016-08/python training/sample.csv',header=0,sep='|')
temp = df.address
df['nikay'] = df['address'].apply(lambda x: re.search(r'Nikay:(.*?),',x).group(1))
df['district'] = df['address'].apply(lambda x: re.search(r'District :(.*)',x).group(1))


2) Python code to  return 'y' if pincode is valid and 'n' if  not valid

def pin_flag(pin_code):
	
	try:
		pin_code = int(pin_code)
		if((pin_code<=299999)&(pin_code>=200000)):
			return('Y')
		else:
			return('N')	
	except ValueError:
		print('do not feed me alpha-numeric')
		return('N')
		
		
def pin_flag2(pin_code):
	pin_code = str(pin_code)
	if(re.search(r'^2\d{5}$',pin_code)):
		return('Y')
	else:
		return('N')

pc=pd.read_csv('D:/Bhatt/2016-08/python training/pincode.csv',header=0,sep='|')
pc['pin_flag']=pc['pincode'].apply(pin_flag)

3) Python code to find the frequency of all the words in a given file

import pandas as pd

def freq_count(file_path):
	file = open(file_path,'r+')
	wordcount={}
	str0=file.read()
	str1=str0.replace('\n',' ')
	str2=str1.replace(',','')
	str3=str2.replace('.','')
	str3=str2.split(' ')
	for word in str3:
		if word not in wordcount:
			wordcount[word] = 1
		else:
			wordcount[word] += 1
	sorted_dict = sorted(wordcount.items(),key = lambda x:x[1],reverse = True)
	sorted_df = pd.DataFrame(sorted_dict)
	sorted_df.columns = ['word','frequency']
	print(sorted_df)

4)  Python code to print the anagram of the given word with reference to a dictionary

def anagram(init_word):
    if len(init_word) <=1:
        return init_word
    else:
        tmp = []
        for perm in anagram(init_word[1:]):
            for i in range(len(init_word)):
                tmp.append(perm[:i] + init_word[0:1] + perm[i:])
        return tmp

perm_list=anagram('may')
f=open('D:/Bhatt/2016-08/python training/sample_dict.txt')
ref_dict=f.read()
ref_dict=ref_dict.split('\n')
for i in perm_list:
 for j in ref_dict:
  if i==j:
   print(i)
   break


5) To print top 3 and bottom/worst 3 male and female names from all html files listed in a given directory

import os
import re
import pandas
	
def parse_top_n(year,n):
	path_name = 'D:/Bhatt/2016-08/python training/babynames/baby'+str(year)+'.html'
	f=open(path_name)
	file_cont = f.read()
	name_list=re.findall(r'<tr align="right"><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',file_cont)
	temp = name_list[0:n]
	temp = pd.DataFrame(temp)
	temp.columns = ['rank','male','female']
	
	temp['rank'] = temp['rank'].astype(int)
	
	female=list()
	male=list()
	
	female= (temp.groupby('female')['rank'].sum())/(temp.groupby('female')['rank'].count())
	female=female.sort_values()
	print("Top 3 Female names")
	print(female[:3])
	print("Worst 3 Female names")
	print(female[-3:])

	male= (temp.groupby('male')['rank'].sum())/(temp.groupby('male')['rank'].count())
	male=male.sort_values()
	print("Top 3 Male names")
	print(male[:3])
	print("Worst 3 Male names")
	print(male[-3:])

6) Python code to generate a histogram pattern given an input of numbers. 

def my_hist(ref_list):
	print('my awesome histogram')
	len_list=ref_list.__len__()
	for i in range(0,max(ref_list)):
		ref_list=for_row(ref_list,len_list)
		
def print_star(index_list):
	temp_str=''
	iter_len=index_list.__len__()
	for i in range(0,iter_len):
		if(index_list[i] == 1):
			temp_str = temp_str + "* "
		else:
			temp_str = temp_str + '   ' 
	print(temp_str)
	
def for_row(ref_list,len_list):
	max_val = max(ref_list)
	out_val = [0]*len_list
	for i in range(0,len_list):
		if(ref_list[i]==max_val):
			ref_list[i] = ref_list[i]-1
			out_val[i]=1
	print_star(out_val)
	return(ref_list)