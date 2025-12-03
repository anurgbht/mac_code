from bs4 import BeautifulSoup
import urllib.request
f = open("C:\\Users\\rakshitav\\Documents\\magnumcollges.txt",'w')
resp=((urllib.request.urlopen('http://magnum.mu.ac.in/wiki/List_of_Mumbai_Colleges').read()))
soup = BeautifulSoup(resp, 'html.parser')
elements = soup.find_all("li")
f.write(("\n".join("{} {}".format((el.get_text()).lower(), " ") for el in elements)))
f.close()
