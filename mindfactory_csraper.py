# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:27:38 2023

@author: Quinn
"""

import requests  # python-requests.org (pip install requests)
from bs4 import BeautifulSoup # scraper
import re #regex
from datetime import datetime #allows us to add current time
import pandas as pd
import math



def mindfactory(kw, start_date, end_date):
    
    kw = kw.split()
    kw1 = "+".join(kw)

    link = 'https://www.mindfactory.de/search_result.php/search_query/'+kw1+'/article_per_page/5'
    getHTML = requests.get(link)
    getHTMLr = getHTML.content # This will give you raw HTML from getLink1TB
    soupify = BeautifulSoup(getHTMLr, 'html.parser')
    
    url_product = []
    url = soupify.findAll('div', {"class":"p"})
    for url_num in url:
        url_product.append( url_num.find('a').get('href'))
            
    url_product = list(set((url_product)))

    url_product1 = []
    for urls in url_product:
        c = re.compile(r'6700')
        if c.search(urls) != None:
            url_product1.append(urls)

    url_product2 = []
    
    for urls in url_product1:
        R = '#reviews'
        urls = urls.replace('search/true/','page/{page_num}/')
        urls = urls+R
        url_product2.append(urls)
    
    
    # use function mindfactory_inner
    def mindfactory_inner(link):
        
        getHTML = requests.get(link)
        getHTMLr = getHTML.content # This will give you raw HTML from getLink1TB
        soupify = BeautifulSoup(getHTMLr, 'html.parser')

        reviews_block = soupify.findAll("div",{"itemprop":"review"})

        product_title = soupify.find("div",{"class":"visible-xs visible-sm"}).text.strip()[:-20]
        date_revs = []
        reviewers = []
        ratings = []
        review_bodys  = []
        helpfuls = []

        for rev in reviews_block:

            date_revs.append(rev.find("div", {"class":"pull-left mat4"}).find_all('span')[1].text.strip()[3:])
            reviewers.append(rev.find("div", {"class":"pull-left mat4"}).find_all('span')[0].text.strip())
            ratings.append(rev.find('span').text.strip()[:1])
            review_bodys.append(rev.find('div',{'class':'row no-gutters mat4 rev-text'}).text.strip())
            helpfuls.append(rev.find("div", {"class":"col-md-12 col-md-6 text-center visible-xs visible-sm mat4"}).text.strip())
        df = pd.DataFrame({'product_title':product_title,'date_revs':date_revs,
                'reviewers':reviewers,'ratings':ratings,'helpfuls':helpfuls,'review_bodys':review_bodys,'link':link})
        
        reviewspage_end_num = 1
        if soupify.find("ul", {"class":"pagination pull-right"}) != None:
            reviewspage_end_num = soupify.find("ul", {"class":"pagination pull-right"}).text.strip()
            reviewspage_end_num = reviewspage_end_num[reviewspage_end_num.find('von')+4:]

        empty = False
        if not reviews_block :
            empty= True
        return [df,empty,reviewspage_end_num]
    
    df = pd.DataFrame()
    for urls in url_product2:
        link = urls
        page_num = 1
        reviewspage_end_num = 1
        while page_num:
            link = urls.replace('{page_num}',str(page_num))
            df_new,empty,num = mindfactory_inner(link)
            if page_num == 1:
                reviewspage_end_num = num
            if page_num == int(reviewspage_end_num)+1 :
                break
            if empty:
                break
            page_num +=1    
            df = pd.concat([df,df_new])

    df['date_revs'] = pd.to_datetime(df['date_revs'], infer_datetime_format=True)
    df_1 = df[df['date_revs'] <= end_date]
    df_2 = df_1[df_1['date_revs'] >= start_date]
    df_3 = df_2.reset_index(drop=True) 
    
    return df_3
    



# df = mindfactory("6700 xt","2022-12-01" )
# df.to_csv('mindfactory_6700xt.csv')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    