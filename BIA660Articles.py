#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Katie Gangeline, Matthew Miller

- Article collection from Second Nexus (Liberal)
"""
from bs4 import BeautifulSoup
import re
import time
import requests

import re
from nltk.corpus import stopwords
import requests
from operator import itemgetter

from sklearn.feature_extraction.text import CountVectorizer

url = 'https://secondnexus.com/news/'

def getLinks(url): # function to get article links from news pages
    pageNum=47 # number of pages to collect, 10 articles per page
    ArticleLinks = [] # list of article links
    for p in range(47,pageNum+1): # for each page 
        html=None
        print(p)
        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'/page/'+str(p) # url for all other pages
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
        if not html:continue # couldnt get the page, ignore
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
        # get all the article divs
        articles=soup.findAll('div', {'class':('col-md-8 no-padding animsition df-content-sticky push-bottom-4 clearfix')}) 
        for article in articles:
            linkChunks=article.findAll('h4',{'class':'article-title'}) 
            for linkChunk in linkChunks:
                link=linkChunk.find('a')
                if link.get('href'): 
                    ArticleLinks += [(link.get('href'))] # add article link to list
    return ArticleLinks 
    
def getText(urls): # function to get text from articles
    file=open('Liberal_articles.txt','w') # new text file "Liberal_articles.txt"
    p=0
    for url in urls:
        print(p)
        allText = '' # string of all text from articles
        html=None
        pageLink=url 
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
        if not html:continue # couldnt get the page, ignore
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
        article=soup.find('div', {'class':'entry-content'}) # get the content div
        txt=article.findAll('p') # get text
        include = True
        for t in txt:
            if 'Page 1 of' in t.text:
                include = False
            if include:
                if t.text.contains("pic.twitter"):
                    continue
                allText += t.text
            # take out "page 1 of..." at the end of each article 
        allText=re.sub('[^0-9A-Za-z]',' ',allText.lower()).strip()
        file.write(allText.replace('\t',' ').replace('\n',' ')+'\t'+'Liberal'+'\n')
        p+=1
    file.close() # add article text to the file along with its label
    
# file = open('Liberal_articles.txt')
'''
def countFreq(file):
    freq={}
    f=file.read()
    sentences=f.split('.') # split the text into sentences 
    stop_words = set(stopwords.words('english'))  
    for sentence in sentences: # for each sentence 
        sentence=sentence.lower().strip() # lower case and strip	
        sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space
        words=sentence.split(' ') # split to get the words in the sentence 
        for word in words: # for each word in the sentence 
            if word in stop_words:continue # ignore stop words
            if word=='':continue # ignore empty words
            else: freq[word]=freq.get(word,0)+1 # update the frequency of the word 
    # sort the dictionary by value, in descending order 
    newFreq = {}
    for word in freq: 
        if freq[word]>=10: 
            newFreq[word]=freq[word] # make a new dict of only words with frequency >= 10
    sortedByValue=sorted(newFreq.items(),key=itemgetter(1),reverse=True)
    print(sortedByValue)
'''

if __name__=='__main__':
    url='https://secondnexus.com/news/'
    urls = getLinks(url) 
    getText(urls)

# file.close()
    
    
    
    
