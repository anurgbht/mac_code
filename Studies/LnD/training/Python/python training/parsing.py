import re
import pandas as pd

f=open('D:/Bhatt/2016-08/python training/babynames/baby1990.html')
file_cont=f.read()
re.search(r'<tr align="right"><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',file_cont).group(1,2,3)
name_list=re.findall(r'<tr align="right"><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',file_cont)

==========================

df = pd.DataFrame(name_list)
df.columns=['rank','male','female']
df.head()
df['rank'] = df['rank'].astype(int)
df['rank2'] = 1001-df['rank']
df['len_male'] = df['male'].str.len()
df['len_female'] = df['female'].apply(lambda x: len(x))
df['length']=df['male'].apply(word_len)
==========================

df=pd.read_csv('D:/Bhatt/2016-08/python training/sample.csv',header=0,sep='|')
temp = df.address
df['nikay'] = df['address'].apply(lambda x: re.search(r'Nikay:(.*?),',x).group(1))
df['district'] = df['address'].apply(lambda x: re.search(r'District :(.*)',x).group(1))

==========================

from bs4 import BeautifulSoup
import urllib.request
f = open("C:\\Users\\rakshitav\\Documents\\magnumcollges.txt",'w')
resp=((urllib.request.urlopen('http://magnum.mu.ac.in/wiki/List_of_Mumbai_Colleges').read()))
soup = BeautifulSoup(resp, 'html.parser')
elements = soup.find_all("li")
f.write(("\n".join("{} {}".format((el.get_text()).lower(), " ") for el in elements)))
f.close()

=========================

def word_len(x):
	return(len(x))
	
========================

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
		
=========================

pc=pd.read_csv('D:/Bhatt/2016-08/python training/pincode.csv',header=0,sep='|')
pc['pin_flag']=pc['pincode'].apply(pin_flag)

=========================

def sum_df(df):
	return df['len_male'] + df['len_female']
	
=========================

df['sum_two'] = df.apply(sum_df,axis=1)