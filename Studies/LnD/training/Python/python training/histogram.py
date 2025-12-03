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