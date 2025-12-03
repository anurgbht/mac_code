def parse_top_n(year,n):
	path_name = 'D:/Bhatt/2016-08/python training/babynames/baby'+str(year)+'.html'
	f=open(path_name)
	file_cont = f.read()
	name_list=re.findall(r'<tr align="right"><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',file_cont)
	temp = name_list[0:n]
	temp = pd.DataFrame(temp)
	temp.columns = ['rank','male','female']
	temp['year']=int(year)
	return(temp)