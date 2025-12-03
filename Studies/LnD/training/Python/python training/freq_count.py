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