def my_head(file_path,n):
	with open(file_path, 'rb') as f:
		x=0
		while (x<n):
			content = f.readline()
			print(content)
			x=x+1
			
def my_head2(file_path):
	f=ps.read_csv(file_path)
	print(f.head()) 

	
def my_head3(file_path,n):
	with open(file_path, 'rb') as f:
		x=0
		