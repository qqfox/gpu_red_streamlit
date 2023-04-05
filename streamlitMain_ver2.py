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
from techpowerup_scraper import techPowerup_main


header = st.container()
features = st.container()
model = st.container()



with header:
    st.header("PowerColor Web scraping Dashboard")
    st.text("This is a demo for scrawping the Reddit and Techpowerup websites.")

    # def handle_click(new_type):
    #     st.session_state.type = new_type

    # def handle_click_wo_button():
    #     if st.session_state.kind_of_column:
    #         st.session_state.type = st.session_state.kind_of_column

    st.session_state['type'] = st.radio("Choose the website to crawl data",['Reddit','Techpowerup'])
    # type_of_colum = st.radio("Choose the website to crawl data",['Reddit','Techpowerup'])
    # change = st.button('Change', on_click = handle_click, arg = [type_of_colum] )
    # type_of_column = st.radio("Choose the website to crawl data",['Reddit','Techpowerup'], on_change = handle_click_wo_button, key = 'kind_of_column')


# process for reddit
    if st.session_state['type'] == "Reddit":

        with st.form(key='my_form_to_submit'):
            
    
            st.text('The format of date should be YYYY-MM-DD. For example: 2023-03-30')

            start_date = st.text_input("Start date input: ")
            end_date = st.text_input("End date input: ")

            
            st.text("Please input the name of gpu card.")
            keyword_1 = st.text_input("For example: 6900 xt")
            keyword_2 = "".join(keyword_1.split())

            st.text("After fill in the information, please press submit button")
            st.text("Then the running man at the top right corner will do excersise until finishs RUNNING.")

            submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            try:
                df = reddit_framework(keyword_1, keyword_2, start_date, end_date)
                
                # display the dataframe
                
                st.write(df.head())

                st.text("If the table is blank, there is no data in the time you request or something went wrong with the input")

                st.text("Esle, please press Download data button to save csv file to you computer")
                
                st.download_button(label = "Download Data", data = df.to_csv(),
                                    file_name = "Reddit_dataset.csv",
                                    mime='text/csv')
            except:
                print('There is somthing wrong with your query')


# process for Techpowerup    
    elif st.session_state['type'] == 'Techpowerup':
        
        with st.form(key='my_form_to_submit'):

            st.text("Please input the link of main forrum: ")
            st.text("if more than two links, please separate by a comma ,")
            urls_lst =  st.text_input("For example, the main forum 'Overclocking & Cooling' should input link:  https://www.techpowerup.com/forums/forums/overclocking-cooling.13/")
        
            st.text("Please input the name of gpu card: ")
            keyword_1 = st.text_input("For example: 6900 xt")  
            keyword_2 = "".join(keyword_1.split())              
              
            
            st.text("The data is crawled if last updated within 3 months.")
            st.text("After fill in the information, please press submit button")
            st.text("Then the running man at the top right corner will do excersise until finishs RUNNING.")
            
            submit_buttonn = st.form_submit_button(label='Submit')
            
        if submit_buttonn:
            
            try:
                crawldata = []
                
                for url in urls_lst:
                    techp1 = techPowerup_main(url,keyword_1)
                    techp2 = techPowerup_main(url,keyword_2)
                    crawldata.append(techp1)
                    crawldata.append(techp2)
                
                fin_tech = pd.concat(crawldata,axis=0)
                
                st.write(fin_tech.head())

                st.text("If the table is blank, there is no data in the time you request or something went wrong with the input")

                st.text("Please press Download data button to save csv file to you computer")

                st.download_button(label = "Download Data", data = fin_tech.to_csv(),
                                    file_name = "Techpowerup_dataset.csv",
                                    mime='text/csv')
        
            
            except:
                print('There is somthing wrong with your query')
            # display the dataframe
                
    else:
        print('Opps')
    
    
    
