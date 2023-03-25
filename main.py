# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 23:31:26 2023

@author: Quinn Quinn
main.py to run all the scripts for all websites
"""

from reddit_scraper import reddit_framework



final_df = reddit_framework("6900 xt","6900xt","2022-11-01","2023-03-31")
final_df.to_csv('final_df_reddit.csv')



