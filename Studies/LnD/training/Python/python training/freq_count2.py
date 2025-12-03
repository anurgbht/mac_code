'''df = pd.read_csv('C:\\Users\\rakshitav\\Documents\hp_trial.csv', sep='|', header=0)



file = open('C:\\Users\\rakshitav\\Documents\hp_trial.csv', r)
file.readline( )


head = [next(file) for x in xrange(N)]
print head'''

file=open("text.txt", "r+")

wordcount={}

str=file.read();
str1=str.replace('\n',' ')
str2=str1.replace(',','')
str3=str2.replace('.','')
str3=str2.split(' ')


for word in str3:
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

for k,v in wordcount.items():
	print(k)
	print(v)
    



  #  'C:\\Users\\rakshitav\\Documents\\ass1.txt'
