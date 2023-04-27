# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:57:21 2023

@author: Quinn
Code: for reddit crawling
"""

import requests
import re
import praw
from datetime import date
import csv
import pandas as pd
import time
import sys


reddit = praw.Reddit(client_id='FBRtuxQGmGgjkpvwYrgXTw',
                     client_secret='dkLHsrhPeLESvPsr9jURZquDhLgBkg',
                     user_agent='gpu_crawl', check_for_async=False)


def get_comments(submission):
    '''
        Submission is an object created using praw API.
    '''
#         Remove all "more comments".
    submission.comments.replace_more(limit=5)
    comments = []
    for each in submission.comments.list():
        try:
            comments.append((each.id, each.link_id[3:], date.fromtimestamp(each.created_utc).isoformat(), each.score, each.body) ) #each.author.name
        except AttributeError as e: # Some comments are deleted, we cannot access them.
            continue
    return comments

def reddit_framework(keyword1, start_date, end_date): # keyword input should be "6900 xt" and "6900xt"
    
    comments = []
    posts = []
    count = 0
    
    keyword2 = "".join(keyword1.split())
    
    list_kw = [str(keyword1), str(keyword2)]

    for kw in (list_kw):
    
        submission = reddit.subreddit('all')
                                            
        for post in submission.search(kw,sort = 'new', limit = 5):
            
            #get the posts, can edit post... below to get expected information 
            posts.append((post.id, post.url, post.num_comments, post.subreddit_name_prefixed, date.fromtimestamp(post.created_utc).isoformat(), post.title, post.selftext))
    
            temp_comments = get_comments(post)
            comments += temp_comments
            count += 1
            if count % 50 == 0:
                time.sleep(60)
    
    # create comments dataframe
    comments_fieldnames = ["comment_id", "submission_id", "comment_time", "comment_score", "comment_text"] # "author_name",
    df_comments = pd.DataFrame(comments, columns=comments_fieldnames)
    
    # create posts dataframe
    submissions_fieldnames = ["submission_id", "url", "num_all_comments", "submission_subreddit", "post_date", "submission_title", "post_text"]
    df_submission = pd.DataFrame(posts, columns=submissions_fieldnames)
    
    inner_join = pd.merge(df_comments, 
                      df_submission, 
                      on ='submission_id', 
                      how ='right')
    
    inner_join_ =  inner_join.drop_duplicates(subset=['comment_id', 'submission_id', 'comment_time', 'comment_score',
       'comment_text', 'url', 'num_all_comments', 'submission_subreddit',
       'post_date', 'submission_title', 'post_text'], keep='first')
    
    start_d = inner_join_["post_date"] >= start_date #"2022-11-01"
    end_d = inner_join_["post_date"] <= end_date     # "2023-01-31"
      
    # filter data between "2022-11-01" to "2023-03-31"
    final_df = inner_join_.loc[start_d & end_d]
    
    return final_df
    


# df = reddit_framework("6700 xt", "2022-11-01", "2023-03-31")










