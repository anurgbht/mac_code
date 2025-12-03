import string
import re

def make_good(s):
    punc = string.punctuation
    s_back=s
    s = s.lower()
    for i in punc:
        s = s.replace(i,' ')
        s = re.sub('[ \t]+',' ',s)
    print(s,s_back)
    return s

def is_valid_phrase(p):
    punc = string.punctuation
    punc = [x for x in punc]
    p=p.lower()
    flag = True
    for i in p:
        if i in punc:
            flag = False
    p = p.split(' ')
    try:
        p.index('')
        flag = False
    except:
        pass
    return flag


def is_phrase_in(phrase,text):
    if is_valid_phrase(phrase):
        phrase = phrase.lower()
        phrase = phrase.split(' ')
        text = make_good(text)
        text = text.split(' ')
        index_phrase = []
        for i in phrase:
            try:
                index_phrase.append(text.index(i))
            except:
                return False
        print(index_phrase)
        for i in range(1,len(index_phrase)):
            if (index_phrase[i-1] == (index_phrase[i] -1)):
                return True
            else:
                return False
    else:
        print('invalid phrase')
        return False
        
    

    
s1="PURPLE COW"
s2='The purple cow is soft and cuddly.'
s4='Purple!!! Cow!!!'
s3='The farmer owns a really PURPLE cow.'
s5='purple@#$%cow'
s6='Did you see a purple        cow?'
i1='Purple cows are cool!'
i2='The purple blob over there is a cow.'
i3='How now brown cow.'
i4='Cow!!! Purple!!!'
i5='purplecowpurplecowpurplecow'
i6="    cow   ! purple \t nn"

vp='purple cow'
ivp = 'purple  cow !'

all_p = [vp,ivp]

all_str = [s1,s2,s3,s4,s5,s6,i1,i2,i3,i4,i5,i6]
good_str=[]

for s in all_str:
    good_str.append(make_good(s))

import datetime

time_str1 = "3 Oct 2016 17:00:10"
time_str2 = "4 Oct 2016 17:00:10"
time_format = "%d %b %Y %H:%M:%S"

tt1 = datetime.datetime.strptime(time_str1,time_format)
tt2 = datetime.datetime.strptime(time_str2,time_format)
