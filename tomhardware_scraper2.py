# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 14:53:09 2023

@author: Quinn
To craw tomhardware forum

"""
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# fillin and search

def tomehardware(kw1, date,driver):
    # path = 'C:\chromedriver.exe'
    # driver = webdriver.Chrome(path)   
    url = 'https://forums.tomshardware.com/search/'
    driver.get(url)
    kw2 = "".join(kw1.split())

    # input keywords search
    time.sleep(2)
    kw_input1 = driver.find_element(By.XPATH,"(//input[@class='input'])[3]")
    kw_input1.clear()
    kw_input1.send_keys(str(kw1)+' OR '+str(kw2))  # Variable 
    
    # check box
    driver.find_element(By.XPATH, "(//input[@name='c[title_only]']/following-sibling::i)[5]").click()
    
    # time range
    time.sleep(2)
    time_input1 = driver.find_element(By.NAME,"c[newer_than]")
    time_input1.clear()
    time_input1.send_keys(date)        # Variable 
    time.sleep(10)
    # submit
    time_input1.submit()
    
    time.sleep(5)
    # crawl data 
    # soup = BeautifulSoup(driver.page_source)
    
    # save url print to url
    from io import StringIO
    import sys
    
    buffer = StringIO()
    sys.stdout = buffer
    print(driver.current_url)
    print_output = buffer.getvalue()
    url_search = print_output[0:-1]
    # sys.stdout = sys.__stdout__
    
    
    
    """
    input: search result source page
    output: Dataframe
    
    """
    ## Create list to pull random intervals from + counter
    
    time_splits = np.linspace(6.129, 20.783, num=40)
    counter = 0
    
    headers  = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    # url_2 = url+'?last_days=90'
    
    s = HTMLSession()
    r = s.get(url_search)
    
    if r.status_code == 200:            
    
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # find number of pages
        try:
            total_no_page= soup.find_all('li', {'class':'pageNav-page'})[-1].text
            
        except:
            total_no_page = '1'
                
    
    # craw all urls of 
    
        page_num = int(total_no_page)
       
        lst_pages_urls = []
        
        for i in range(1,page_num+1):
            # split url to add in page number
            url_search1, url_search2 = url_search.split('/?', 1)
                   
            lst_url = url_search1 + str('/?page=') + str(i) +str('&') + url_search2
            lst_pages_urls.append(lst_url)
        
    # crawl all posts information
        crawlData = []
        
        for link in lst_pages_urls:
        
            r1 = requests.get(link, headers = headers)
        
            soup4 = BeautifulSoup(r1.text, "html.parser")
            
            tech_posts = soup4.find_all('div', {'class':'contentRow-main'})
            
            for item in tech_posts:
                # title =  item.a.string
       
                url2= 'https://forums.tomshardware.com' + item.a['href']
                r2 = s.get(url2)
                soup3 = BeautifulSoup(r2.text, 'html.parser')
                
                try:
                    total_no_page2= soup3.find_all('li', {'class':'pageNav-page'})[-1].text
                    
                except IndexError:
                    total_no_page2 = '1'
                        
                
                # create all url from name of forum and number of pages
                
                page_num = int(total_no_page2)                        
                lst_pages_urlss = []
                
                for i in range(1,page_num+1):
                    lst_url = url2+'page-'+str(i)
                    lst_pages_urlss.append(lst_url)
                    
                
                titles = []
                posts = []
                postDates = []
                comments = []
                urls = []
                
                for link in lst_pages_urlss:
                    r3 = s.get(link)
                    soup2 = BeautifulSoup(r3.text, 'html.parser')
                    
                    selects = soup2.findAll('blockquote')
                    for match in selects:
                        match.decompose()
                        
                       
                    post_title = soup2.find("h1", {"class":"p-title-value"}).text.strip()
                    if 'page-1' in link: # avoid duplicate
                        post_content = soup2.find("div",{"class":"bbWrapper"}).text.strip()
                        post_date = soup2.find("time",{"class":"u-dt"}).text.strip()
                        
                        
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
    
    driver.quit()
    crawlDataframe = pd.concat(crawlData,axis=0)


    return crawlDataframe



# run the code
# df = tomehardware("6700 xt", '2022-12-01')





