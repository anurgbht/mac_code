def freq_anal(file_path):
	with open(file_path, 'rb') as f:
		content = f.readlines()
	long_string = ''
	for i in range(0,4):
		long_string = long_string + content[i]
		
	long_string = long_string.replace('\n',' ')
	long_string = long_string.replace('\r',' ')
	long_string = long_string.replace(',','')
	long_string = long_string.replace('.','')
	return(long_string)
	
	
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

def anagram(init_word):
    if len(init_word) <=1:
        return init_word
    else:
        tmp = []
        for perm in anagram(init_word[1:]):
            for i in range(len(init_word)):
                tmp.append(perm[:i] + init_word[0:1] + perm[i:])
        return tmp