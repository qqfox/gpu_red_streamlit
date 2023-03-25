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
dataset = st.container()
features = st.container()


with header:
    st.header("PowerColor Web scraping Dashboard")
    st.text("This is a demo for scrawping the Reddit website. Other website will be developed in April")
    
    
# with features:
#     st.text("""Define the range of time for crawling. The format of date should be like "2023-03-31" """)
#     input_feature = sel_col.text_input()


# layout 
col1, col2 =st.columns(2)

with features:
    with col1:
        d1 = st.date_input("Define the start date for crawling.")
            #datetime.date(2023,3,1))
        start_date = st.write('Start date:', d1)
    with col2:
        d2 = st.date_input("Define the end date for crawling.")
                           #datetime.date(2023,3,1))
        end_date = st.write('End date:', d2)
    
    keyword_1 = st.text_input("Please input the name of gpu card: (ex: 6900 xt")
    keyword_2 = st.text_input("Please input the name of gpu card: (ex 6900xt")
    
    df = reddit_framework(keyword_1, keyword_2, start_date, end_date)
    
    # display the dataframe
    
    st.write(df.head())
    
    st.download_button(label = "Download Data", data = df.to_csv(),
                       file_name = "Reddit_dataset.csv",
                       mime='text/csv')
    
    
    
    