# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 16:54:33 2018

@author: O345
"""

from bs4 import BeautifulSoup
import re
import time
import requests
from selenium import webdriver


def getText(url):
    
    html=None

    for i in range(5): # try 5 times
        try:
            #use the browser to access the url
            response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html=response.content # get the html
            break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt',i)
            time.sleep(2) # wait 2 secs

    #if not html: continue # couldnt get the page, ignore
        #print(html)
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
    
    articleBody=soup.find('div', {'class':re.compile('article-body')}) # get all the review divs
    content2=articleBody.findAll('p')
    ret=""
    for i in content2:
        ret = ret + i.text.strip('\n').strip('\t')
        
    return ret
        
def genLinks(url):
    html=None
    url='https://www.foxnews.com/politics'

    #open the browser and visit the url
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    
    #scroll down twice to load more tweets
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    loadMore=driver.find_element_by_css_selector('div.button.load-more')
    
    for i in range(10):
        loadMore.click()
        time.sleep(2)

    html=driver.page_source
    

    #if not html: continue # couldnt get the page, ignore
    #print(html)
    #soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
    soup = BeautifulSoup(html,"lxml") # parse the html 

    fw = open('train_Fox.txt', 'w')
    article_list = soup.findAll('div', {'class':re.compile('content article-list')})
    
    for alist in article_list:
        #print(len(alist))
        articles = alist.findAll('article', {'class':re.compile('article')})
        #print(articles[0])
        ret_text = ""
        for article in articles:
            #print(article)
            if len(article['class']) > 1:
                continue
            
            link = article.find('a')['href']
            if 'video' in link:
                continue
            link = "https://www.foxnews.com"+link
            #print(link)
            #print('\n')
            ret_text=ret_text + getText(link) + '\t' + "Conservative" + '\n'
    fw.write(ret_text)
    fw.close()

if __name__=='__main__':
    #url='https://www.foxnews.com/politics/house-democrats-reportedly-preparing-subpoena-cannon-for-trump-related-probes'
    url_alist='https://www.foxnews.com/politics'
    genLinks(url_alist)

