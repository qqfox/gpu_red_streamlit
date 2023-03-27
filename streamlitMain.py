# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 23:23:04 2023

@author: Quinn Quinn
"""

import streamlit as st
import datetime
import requests
import re
import praw
from datetime import date
import csv
import pandas as pd
import time
import sys

from reddit_scraper import reddit_framework

header = st.container()
features = st.container()
model = st.container()


# with header:
#     st.header("PowerColor Web scraping Dashboard")
#     st.text("This is a demo for scrawping the Reddit website. Other website will be developed in April")

# with features:
#     st.text("Input crawling information following below example")
#     st.text(""" "6900 xt","6900xt","2022-11-01","2023-03-31" """)

#     key_input = st.text_input("Please input the information")
    
# with model:
    
#     df = reddit_framework(key_input)
    
#     # display the dataframe
#     st.text('Sample of data')
#     st.write(df.head())
    
#     st.download_button(label = "Download Data", data = df.to_csv(),
#                        file_name = "Reddit_dataset.csv",
#                        mime='text/csv')

with header:
    st.header("PowerColor Web scraping Dashboard")
    st.text("This is a demo for scrawping the Reddit website. Other website will be developed in April")
    
    

with features:

    # d1 = st.date_input("Define the start date for crawling.")
    # start_date = st.write('Start date:', d1)
    start_date = st.text_input("Start date input: ")
    end_date = st.text_input("End date input: ")

    # d2 = st.date_input("Define the end date for crawling.")
    # end_date = st.write('End date:', d2)
    
    keyword_1 = st.text_input("Please input the name of gpu card: (ex: 6900 xt)")
    keyword_2 = st.text_input("Please input the name of gpu card: (ex 6900xt)")
    
    
    
with model:
    
    df = reddit_framework(str(keyword_1), str(keyword_2), str(start_date), str(end_date))
    
    # display the dataframe
    
    st.write(df.head())
    
    st.download_button(label = "Download Data", data = df.to_csv(),
                        file_name = "Reddit_dataset.csv",
                        mime='text/csv')
    
    
    
    
