
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 15:55:29 2021

@author: emari
"""

import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager

def get_tweet_data(card):
    username = card.find_element_by_xpath('./div[2]/div[1]//span').text
    handle = card.find_element_by_xpath('./div[2]/div[1]//span[contains(text(), "@")]').text
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding 
    reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    tweet = (username, handle, postdate, text, reply_count, retweet_count, like_count)
    return tweet

#options = EdgeOptions()
#options.use_chromium = True
driver = webdriver.Chrome(ChromeDriverManager().install())#Edge(options = options)

driver.get('https://twitter.com/login')
sleep(1)

#Username
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('StephanoCallie')

#passwordHardcodedForFullAutomation
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys('1password1')
password.send_keys(Keys.RETURN)
sleep(2)

#TakingInputFromTopOfTrendingPage
search_input = driver.find_elements_by_xpath('//header[@role="banner"]')
search_input = driver.find_element_by_xpath('//a[@href="/explore"]').click()
sleep(3)

search_input = driver.find_element_by_xpath('//a[@href="/explore/tabs/trending"]').click()

sleep(3)
postnum = 0
postnum+=4
driver.find_element_by_css_selector("#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div.css-1dbjc4n.r-1jgb5lz.r-1ye8kvj.r-13qz1uu > div > div > section > div > div > div:nth-child({0}) > div >  div > div > div:nth-child(2) > span".format(postnum)).click()

sleep(1)
scroll_attempt = [0]
    
    
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
                
    scroll_attempt.append(0)
    while True:
        #print("I got here")
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            print("I got here")
            scroll_attempt[len(scroll_attempt)-1] += 1
            
            if scroll_attempt[len(scroll_attempt)-1] >= 3:
                print("I got here 2")
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = curr_position
            #break