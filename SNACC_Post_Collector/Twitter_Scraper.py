#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import os
import wget
import sys
sys.path.append("..\SNACC_Mapper\.")
from trend_node import node
from trend_node import nodeClassifier

global node_db 
node_db = nodeClassifier()

class Twitter_Scrape():
    def get_tweet_data(card,input_node):
        bufferNode = input_node
        username = card.find_element_by_xpath('./div[2]/div[1]//span').text
        bufferNode.username = username
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        caption = comment + responding 
        bufferNode.captions.append(caption)

        like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        bufferNode.total_likes+=like_count



        reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text

        retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text


        tweet = (username, postdate, caption, reply_count, retweet_count, like_count)
        return tweet


    driver = webdriver.Chrome(ChromeDriverManager().install())

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

        scroll_attempt = 0
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2)
            else:
                last_position = curr_position
                break

    sleep(5)


    with open('TS_op.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Comments', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    driver.close()
    sleep(5)

    #Get top usersers on Twitter

    def get_toptweet_data(card, i, input_node): 
        
        username = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[' + str(i + 1) + ']/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[1]/div[1]').text
        
        
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        comment = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[' + str(i + 1) + ']/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        caption = comment + responding 
        
        
        like_count = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[' + str(i + 1) + ']/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div/div[2]').text
        
        
        reply_count = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[' + str(i + 1) + ']/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]').text
        retweet_count = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[' + str(i + 1) + ']/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/div[2]').text
        
        tweet = (username, postdate, caption, reply_count, retweet_count, like_count)
        return tweet

    sleep(5)

    top_data = []
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get('https://friendorfollow.com/twitter/most-followers/')
    sleep(1)    

    for i in range(100):
        search_input = driver.find_element_by_xpath('/html/body/main/div/div/div[2]/ul/li[' + str(i+1) + ']/div[1]/p[1]/a').click()
        sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        sleep(8)
        for i in range(3):
            main_body = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main')
            tweets_tab = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/nav/div/div[2]/div/div[1]/a')
            cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

            card = cards[i]

            try:
                tweet = get_toptweet_data(card, i, input_node)
                top_data.append(tweet)
            except NoSuchElementException:
                i+=1
                tweet = get_toptweet_data(card, i, input_node)
                top_data.append(tweet)

        sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)

    with open('Top_users.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Comments', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(top_data)

