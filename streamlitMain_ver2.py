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
from tomhardware_scraper import tomehardware


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
    # type_of_column = st.radio("Choose the website to crawl data",['Reddit','Techpowerup','Tomhardware'])
    
    st.session_state.name = st.session_state.get('Reddit')
    st.session_state.phone = st.session_state.get('Techpowerup')
    st.session_state.phone = st.session_state.get('Tomhardware')
    with st.sidebar:
        radio = st.radio(
        "Please select",
        ('Reddit', 'Phone','Tomhardware'))
        

# process for reddit
    # if st.session_state['type'] == "Reddit":
    if radio == "Reddit":

        with st.form(key='my_form_to_submit'):
    
            # d1 = st.date_input("Define the start date for crawling.")
            # start_date = st.write('Start date:', d1)
            start_date = st.text_input("Start date input: ")
            end_date = st.text_input("End date input: ")
        
            # d2 = st.date_input("Define the end date for crawling.")
            # end_date = st.write('End date:', d2)
            
            keyword_1 = st.text_input("Please input the name of gpu card: (ex: 6900 xt)")
            keyword_2 = "".join(keyword_1.split())
            
            submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            try:
                df = reddit_framework(keyword_1, keyword_2, start_date, end_date)
                
                # display the dataframe
                
                st.write(df.head())
                
                st.download_button(label = "Download Data", data = df.to_csv(),
                                    file_name = "Reddit_dataset.csv",
                                    mime='text/csv')
            except:
                print('There is somthing wrong with your query')
# process for Techpowerup    
    # if st.session_state['type'] == 'Techpowerup':
        if radio == "Techpowerup":

            
            
            with st.form(key='my_form_to_submit'):
                st.text("This website does not have search function.")
                st.text("Therefore, you need to fill in the links of forums you want to crawl, if more than two links, please separate by a comma , ")
                st.text("For example: https://www.techpowerup.com/forums/forums/amd-ati-gpus.58/, https://www.techpowerup.com/forums/forums/overclocking-cooling.13/")

                urls_lst =  st.text_input("Please input links of forum here ")
            
                st.text("Please input the name of gpu card: ")
                keyword_1 = st.text_input("For example: 6900 xt")                
                
                st.text("The data is crawled if it is last updated within 3 months. ")
                submit_button = st.form_submit_button(label='Submit')
                
            if submit_button:
                
                try:
                    crawldata = []
                    
                    for url in urls_lst:
                        techp = techPowerup_main(url,keyword_1)
                        crawldata.append(techp)
                    
                    
                    fin_tech = pd.concat(crawldata,axis=0)
                    
                    st.write(fin_tech.head())
                    
                    st.download_button(label = "Download Data", data = fin_tech.to_csv(),
                                        file_name = "Techpowerup_dataset.csv",
                                        mime='text/csv')
            
                
                except:
                    print('There is somthing wrong with your query')
                # display the dataframe
                
# Process for Tomhardware
    
    # elif st.session_state['type'] == 'Tomhardware':
    if radio == 'Tomhardware':

        
        with st.form(key='my_form_to_submit'):


            st.text("Key in the date and search keywords.")

            st.text("Please input the search keyword here: ")
            keyword = st.text_input("For example: 6900 xt")      
            start_date = st.text_input("Newer than date: ")
            submit_button = st.form_submit_button(label='Submit')
            
        if submit_button:
            with st.echo():
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager

                @st.experimental_singleton
                def get_driver():
                    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

                options = Options()
                options.add_argument('--disable-gpu')
                options.add_argument('--headless')

                driver = get_driver()
                try:
                    df = tomehardware(keyword,start_date,driver=driver)
                    
                    # display the dataframe
                    
                    st.write(df.head())
                    
                    st.download_button(label = "Download Data", data = df.to_csv(),
                                        file_name = "Tomhardware_dataset.csv",
                                        mime='text/csv')
                except:
                    print('There is somthing wrong with your query')
        


    

    
