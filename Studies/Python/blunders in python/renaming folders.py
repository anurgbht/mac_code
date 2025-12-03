import os

os.chdir("E:/Videos/Series/BoJack Horseman/Season 2/")
#.S02E01.Brand.New.Couch.mkv
rt = 'BoJack Horseman'
st = ''

for fname in os.listdir():
    os.rename(fname,fname.replace(rt,st))

