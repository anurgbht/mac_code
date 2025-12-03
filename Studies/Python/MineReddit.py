#! /usr/bin/python3
import os
import praw
import pandas as pd
import datetime as dt

#########################################################################################
#########################################################################################
#########################################################################################


def get_date(created):
    return dt.datetime.fromtimestamp(created)


#########################################################################################
#########################################################################################
#########################################################################################

root_path = os.path.join(os.path.abspath(__file__), "..")

PERSONAL_USE_SCRIPT_14_CHARS = "2JICETwBJDvM5g"
SECRET_KEY_27_CHARS = "eCzNuO-7rQIEYdT318vFEekvjnQ"
APP_NAME = "AnuragPersonalBot"
REDDIT_USER_NAME = "KeepMarxAlive"
REDDIT_LOGIN_PASSWORD = "5Rq32))&"

reddit = praw.Reddit(
    client_id=PERSONAL_USE_SCRIPT_14_CHARS,
    client_secret=SECRET_KEY_27_CHARS,
    user_agent=APP_NAME,
    username=REDDIT_USER_NAME,
    password=REDDIT_LOGIN_PASSWORD,
)

subreddit = reddit.subreddit("Jokes")
top_subreddit = subreddit.top(limit=50)

# topics_dict = { "title":[],"score":[],"id":[], "url":[],"comms_num": [],"created": [],"body":[]}
topics_dict = {"title": [], "score": [], "url": [], "created": [], "body": []}

for submission in top_subreddit:

    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    # topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    # topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)

_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp=_timestamp)

topics_data.to_excel(os.path.join(root_path, "tempExtract.xlsx"))
