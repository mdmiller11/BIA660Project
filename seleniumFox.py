# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 19:32:20 2018

@author: O345
"""
from selenium import webdriver
import time


url='https://www.foxnews.com/politics'

#open the browser and visit the url
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)

#scroll down twice to load more tweets
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

loadMore=driver.find_element_by_css_selector('div.button.load-more')

for i in range(1000):
    loadMore.click()
    time.sleep(2)


