# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 23:13:08 2023

@author: USER
"""

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

from datetime import datetime, timedelta


# Find number of pages

def techPowerup_main(url, kw):
    
    """
    input: mainforum url
    ex: 'https://www.techpowerup.com/forums/forums/networking-security.55/'
    return dataframe of 
    
    """
    ## Create list to pull random intervals from + counter
    time_splits = np.linspace(3.129, 6.783, num=40)
    counter = 0
    
    headers  = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    
    url_2 = url+'?last_days=90'
    
    s = HTMLSession()
    r = s.get(url_2)
    if r.status_code == 200:            
    
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # find number of pages
        try:
            total_no_page= soup.find_all('li', {'class':'pageNav-page'})[-1].text
            
        except IndexError:
            total_no_page = '1'
                
    
    # create all url from name of forum and number of pages
    
        page_num = int(total_no_page)
            
        lst_pages_urls = []
        
        for i in range(1,page_num+1):
            lst_url = url+'page-'+str(i)+'?last_days=90'
            lst_pages_urls.append(lst_url)
        

        crawlData = []
        
        df_blank = pd.DataFrame(columns=['Title','Post body','Date of Post','Comments','Links'])
        crawlData.append(df_blank)
        
        for link in lst_pages_urls:
        
            r1 = requests.get(link, headers = headers)
        
            soup4 = BeautifulSoup(r1.text, "html.parser")
            
            tech_posts = soup4.find_all('div', {'class':'structItem-title'})
            
            for item in tech_posts:
                title =  item.a.string
                if str(kw) or str("".join(kw.split())) in title:
        
                    url= 'https://www.techpowerup.com' + item.a['href']
                    r2 = s.get(url)
                    soup3 = BeautifulSoup(r2.text, 'html.parser')
                    
                    try:
                        total_no_page2= soup3.find_all('li', {'class':'pageNav-page'})[-1].text
                        
                    except IndexError:
                        total_no_page2 = '1'
                            
                    
                    # create all url from name of forum and number of pages
                    
                    page_num = int(total_no_page2)                        
                    lst_pages_urls = []
                    
                    for i in range(1,page_num+1):
                        lst_url = url+'page-'+str(i)
                        lst_pages_urls.append(lst_url)
                        
                    
                    titles = []
                    posts = []
                    postDates = []
                    comments = []
                    urls = []
                    
                    for link in lst_pages_urls:
                        r3 = s.get(link)
                        soup2 = BeautifulSoup(r3.text, 'html.parser')
                        
                        selects = soup2.findAll('blockquote')
                        for match in selects:
                            match.decompose()
                            
                           
                        post_title = soup2.find("h1", {"class":"p-title-value"}).text.strip()
                        
                        if 'page-1' in link:
                            post_content = soup2.find("div",{"class":"bbWrapper"}).text.strip()
                            post_date = soup2.find("time",{"itemprop":"datePublished"}).text.strip()
                            
                            
                            if 'Yesterday' in post_date:
                                post_date = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
                            
                            if 'Today' in post_date:
                                post_date =  datetime.today().strftime('%Y-%m-%d')
                            

                        else:
                            post_content = post_content
                            post_date = post_date
                        
                        discuss_content = soup2.findAll("div",{"class":"bbWrapper"})
                        
                        comment_text = []
                        for i in discuss_content:
                            comment_text.append(i.get_text())
                        
                        titles.append(post_title)
                        posts.append(post_content)
                        postDates.append(post_date)
                        comments.append(comment_text)
                        urls.append(link)
                        
                    df = pd.DataFrame(
                        {'Title': titles,
                         'Post body': posts,
                         'Date of Post': postDates,
                         'Comments': comments,
                         'Links' : urls
                        })
                    
                    crawlData.append(df) # merge dataframe
                    
                    # prevent block by sleep randomly
                    counter += 1
                    alarm = np.random.choice(time_splits)
                    rounding = np.random.choice(list(range(2,6)))
                    print(f'Sleeping {round(alarm, 2)} seconds...')
                    time.sleep(round(alarm, rounding))

                else:
                    continue
        
        crawlDataframe = pd.concat(crawlData,axis=0)
        
    else:
        print('Something wrong with link')
        
    return crawlDataframe 

# example 
# a = techPowerup_main('https://www.techpowerup.com/forums/forums/intel-arc-gpus.94/','A770')