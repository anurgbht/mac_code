def all_babynames(n):
	list_year=range(1990,2009,2)
	temp = pd.DataFrame()
	for i in range(0,len(list_year)):
		temp = temp.append(parse_top_n(list_year[i],n),ignore_index=True)
	#return(temp)
	male = temp['male']
	female = temp['female']
	male_temp = male.value_counts()
	female_temp = female.value_counts()
	print(male_temp.head(1))
	print(female_temp.head(1))