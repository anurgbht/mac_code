import re

line = '4 [label="X[14] <= 0.003\ngini = 0.018\nsamples = 215\nvalue = [2, 213]"] ;'
line = line.replace("\n","")
print(line)
#line = "value = me"
tt = re.search(r'X\[\d+\]',line,re.M)

if tt:
   print("Okay")
   print(tt.group(1))
else:
   print("No match!!")
