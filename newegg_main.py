# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 01:26:43 2023

@author: Quinn
dataframe of products
- product name
- link
- star
- review
    - date review
    - like or dislike review 
"""

import requests  # python-requests.org (pip install requests)
from bs4 import BeautifulSoup # scraper
import re #regex
import pandas as pd
import math
# currentDate = datetime.now().strftime('%Y-%m-%d')
import numpy as np
from time import sleep
from selenium import webdriver
from requests_html import HTMLSession
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


def product_urls(kw):
    
    """
    input: keyword search
    output: list of all related products link
    """
    
    link = 'https://www.newegg.com/p/pl?d='+str(kw)  # variable
    getHTML = requests.get(link)
    getHTMLr = getHTML.content # This will give you raw HTML from getLink1TB
    soupify = BeautifulSoup(getHTMLr, 'html.parser')
    
    # get all the link of products
    items = soupify.findAll('span', {"class":"list-tool-pagination-text"})[-1].text
    print(items)
    items_str = items
    page_end_num = int(items_str[items_str.find('/')+1])
    print(page_end_num )
    
    url_list = []
    for page_num in range(1,page_end_num+1):
        link = f'https://www.newegg.com/p/pl?d=6700xt&page={page_num}' 
        getHTML = requests.get(link)
        getHTMLr = getHTML.content # This will give you raw HTML from getLink1TB
        soupify = BeautifulSoup(getHTMLr, 'html.parser')
        url = soupify.findAll('div',{"class":"item-info"})
        for url_num in url:
            url_list.append(url_num.find('a',{"class":"item-title"}).get('href'))
    
    # filter not related products
    url_list1 = [] # final using list of product links
    for urls in url_list:
        c = re.compile(kw)  # variable
        if c.search(urls) != None:
            url_list1.append(urls)
    return url_list1

def newegg(link):
    driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # define scroll down function 
    def scroll_down():
        """Function to scroll the html page down"""
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to scroll the page down
            sleep(5)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

    # define next page function
    def next_page():
        """Function to go to the next page"""
        sleep(1) # to act like human
        next_button = driver.find_element(By.XPATH,"(//button[@class='btn'])[3]")
        next_button.click()
    
    """
    input: link of one product
    output: dataframe of information
    """

    
    
    driver.get(link)
    sleep(7)
    
    # here you need to close region popup manually
    scroll_down()
    
    # trying to access the review button, Note: sometimes there is no review button in newegg website
    try:
        reviews_button =driver.find_element(By.XPATH,"(//a[@class='tab-nav'])[3]") 
        reviews_button.click()
        sleep(8) 
    except:
        pass
    # select date posted sort
    try:
        date_dropdwn = driver.find_element(By.XPATH, "//label[@class='form-select no-margin']//select[1]")
        dd = Select(date_dropdwn)
        dd.select_by_visible_text("Date Posted")
        
        scroll_down()
        sleep(2)
        
        # select 100 size
        size_dropdwn = driver.find_element(By.XPATH, "(//label[@class='form-select']//select)[1]")
        ss = Select(size_dropdwn)
        ss.select_by_visible_text("100")
        
        # crawl the review information 
        comments_name = []
        date = []
        rating = []
        comments_content = []
        comments_title_content = []
        comments_helpful_like = []
        comments_helpful_unlike = []
        comment = []
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        comments_block = soup.find_all("div", {"class": "comments"})
        
        
        
        for rev in comments_block:
            comment = rev.find_all("div", {"class": "comments-cell has-side-left is-active"})
            
            for comment in comment:
        
        #         print(comment)
                comments_name.append(comment.find("div", {"class": "comments-name"}).text.strip())
                comments_content.append(comment.find("div", {"class": "comments-content"}).text.strip())
                helpful = comment.find_all("div", {"class": "comments-helpful"})
                try:
                    like = helpful[0].find("span").text.strip()
                except:
                    like = 0
                try:
                    unlike = helpful[1].find("span").text.strip()
                except:
                    unlike = 0
                comments_helpful_like.append(like)
                comments_helpful_unlike.append(unlike)
                date.append(comment.find("span", {"class": "comments-text"}).text.split()[0])
            #         print(date)
        
                title_content = comment.find("div", {"class": "comments-title"})
                comments_title_content.append(title_content.find("span", {'class':'comments-title-content'}).text)
                rating_num = title_content.find("i", {'class':'rating'})
                rating = int(re.search(r'\d+', rating_num['class'][1]).group())
            #         print(rating)
            product_title = soup.find("h1",{"class":"product-title"}).text.strip()
    
        
        df = pd.DataFrame({'product_title':product_title,'comments_name':comments_name,
                'date':date, 'rating':rating,'comments_title_content':comments_title_content,
                'comments_content':comments_content,'comments_helpful_like':comments_helpful_like,
                'comments_helpful_unlike':comments_helpful_unlike, 'link':link})
    except:
        # crawl the review information 
        comments_name = []
        date = []
        rating = []
        comments_content = []
        comments_title_content = []
        comments_helpful_like = []
        comments_helpful_unlike = []
        comment = []
               
        non_info = "No review"
        comments_name.append(non_info)
        date.append(non_info)
        rating.append(non_info)
        comments_content.append(non_info)
        comments_title_content.append(non_info)
        comments_helpful_like.append(non_info)
        comments_helpful_unlike.append(non_info)
        comment.append(non_info)
        product_title = link
        link = link
        
        
        df = pd.DataFrame({'product_title':product_title,'comments_name':comments_name,
                'date':date, 'rating':rating,'comments_title_content':comments_title_content,
                'comments_content':comments_content,'comments_helpful_like':comments_helpful_like,
                'comments_helpful_unlike':comments_helpful_unlike, 'link':link})
        
    sleep(60)
    def tearDown(self):
        self.driver.quit()

    
    return df


list_links = product_urls("6700xt")

dfs = []
for link in list_links:
    df = newegg(link)
    dfs.append(df)
    
new_egg = pd.concat(dfs) 
new_egg_final = new_egg.reset_index()
# df['date_revs'] = pd.to_datetime(df['date_revs'], infer_datetime_format=True)
# df_1 = df[df['date_revs'] <= end_date]
# df_2 = df_1[df_1['date_revs'] >= start_date]
# df_3 = df_2.reset_index(drop=True)

# link = 'https://www.newegg.com/asrock-radeon-rx-6700-xt-rx6700xt-cld-12go/p/N82E16814930059?Description=6700xt&cm_re=6700xt-_-14-930-059-_-Product'
# df = newegg(link)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


