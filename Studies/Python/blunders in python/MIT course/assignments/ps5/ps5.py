# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description  = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def evaluate(self,text):
        self.text = text
        return self.is_phrase_in(self.text,self.phrase)
    def is_phrase_in(self,text,phrase):
        if self.is_valid_phrase(phrase):
            phrase = phrase.lower()
            phrase = phrase.split(' ')
            text = self.make_good(text)
            text = text.split(' ')
            index_phrase = []
            for i in phrase:
                try:
                    index_phrase.append(text.index(i))
                except:
                    return False
##            print(index_phrase)
            for i in range(1,len(index_phrase)):
                if (index_phrase[i-1] == (index_phrase[i] -1)):
                    return True
                else:
                    return False
        else:
            print('invalid phrase')
            return False
    def is_valid_phrase(self,p):
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
    def make_good(self,s):
        punc = string.punctuation
        s_back=s
        s = s.lower()
        for i in punc:
            s = s.replace(i,' ')
            s = re.sub('[ \t]+',' ',s)
##        print(s,s_back)
        return s

    
        

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self,phrase):
        PhraseTrigger.__init__(self,phrase)
    def evaluate(self,news_object):
        self.text = news_object.get_title()
        return self.is_phrase_in(self.text,self.phrase)
    

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self,phrase):
        PhraseTrigger.__init__(self,phrase)
    def evaluate(self,news_object):
        self.text = news_object.get_description()
        return self.is_phrase_in(self.text,self.phrase)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self,time_EST):
        self.time_EST = self.convert_to_standard(time_EST)
    def convert_to_standard(self,time_EST):
        try:
            time_format = "%d %b %Y %H:%M:%S"
            time_EST = datetime.strptime(time_EST, time_format)
            time_EST = time_EST.replace(tzinfo=pytz.timezone("EST"))
            return time_EST
        except:
            print("Wrongly formatted string")
            return None
    

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self,time_EST):
        TimeTrigger.__init__(self,time_EST)
    def evaluate(self,other_time):
        self.other_time = other_time.get_pubdate()
        self.other_time = self.other_time.replace(tzinfo=pytz.timezone("EST"))
        time_delta = self.other_time - self.time_EST
        time_delta = time_delta.total_seconds()
        if time_delta < 0:
            return True
        else:
            return False
        
class AfterTrigger(TimeTrigger):
    def __init__(self,time_EST):
        TimeTrigger.__init__(self,time_EST)
    def evaluate(self,other_time):
        self.other_time = other_time.get_pubdate()
        self.other_time = self.other_time.replace(tzinfo=pytz.timezone("EST"))
        time_delta = self.other_time - self.time_EST
        time_delta = time_delta.total_seconds()
        if time_delta > 0:
            return True
        else:
            return False        
    

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(object):
    def __init__(self,trigger_element):
        self.T = trigger_element
    def evaluate(self,news_item):
        self.news_item = news_item
        return not self.T.evaluate(self.news_item)

# Problem 8
# TODO: AndTrigger
class AndTrigger(object):
    def __init__(self,trigger_element1,trigger_element2):
        self.T1 = trigger_element1
        self.T2 = trigger_element2
    def evaluate(self,news_item):
        self.news_item = news_item
        return ((self.T1.evaluate(self.news_item)) and (self.T2.evaluate(self.news_item)))
# Problem 9
# TODO: OrTrigger

class OrTrigger(object):
    def __init__(self,trigger_element1,trigger_element2):
        self.T1 = trigger_element1
        self.T2 = trigger_element2
    def evaluate(self,news_item):
        self.news_item = news_item
        return ((self.T1.evaluate(self.news_item)) or (self.T2.evaluate(self.news_item)))

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    print(len(stories),len(triggerlist))
    print(triggerlist)
    stories_return = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                stories_return.append(story)
##    return stories_return
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

