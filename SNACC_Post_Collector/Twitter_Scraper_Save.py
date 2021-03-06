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
import string
import os
import wget
import sys
sys.path.append("..\SNACC_Mapper\.")
from trend_node import node
from trend_node import nodeClassifier

global node_db 
node_db = nodeClassifier(r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Post_Collector')

class Twitter_Scrape():
    def __init__(self,KEYWORD):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.login()
        self.navigate(KEYWORD)
        node_db.exportNetwork()
        #self.get_toptweet_data(card, i)
        #self.topusers()
        
    def get_tweet_data(self,card):
        bufferNode = node()
        
        username = card.find_element_by_xpath('./div[2]/div[1]//span').text
        handle = card.find_element_by_xpath('./div[2]/div[1]//span[contains(text(), "@")]').text
        handle = handle.replace('@','')
        bufferNode.username = handle
        bufferNode.parent_node = handle
        bufferNode.connection_type = 'ROOT'
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        caption = comment + responding 
        bufferNode.captions.append(caption)
        like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        if 'K' in like_count:
            like_buffer = like_count
            like_buffer = like_buffer.replace('K','')
            like_buffer = like_buffer.split('.')
            print(like_buffer)
            try:
                like_int = like_buffer[0] + like_buffer[1]+'00'
            except:
                like_int = like_buffer[0] + '000'
            bufferNode.total_likes+=int(like_int)   
        else:
            try:
                bufferNode.total_likes+=int(like_count)
            except:
                pass
            
        reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        
        tweet = (username, postdate, caption, reply_count, retweet_count, like_count)
        node_db.addNode(bufferNode)
        return tweet

    def login(self):

        self.driver.get('https://twitter.com/login')
        sleep(1)

        #Username
        username = self.driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username.send_keys('JKarnol')

        #passwordHardcodedForFullAutomation
        password = self.driver.find_element_by_xpath('//input[@name="session[password]"]')
        password.send_keys('^2pNVT%ttzuoX')
        password.send_keys(Keys.RETURN)
        sleep(2)

    def navigate(self,KEY):
        #TakingInputFromTopOfTrendingPage
        #search_input = self.driver.find_elements_by_xpath('//header[@role="banner"]')
        #search_input = self.driver.find_element_by_xpath('//a[@href="/explore"]').click()
        sleep(5)

        #search_input = self.driver.find_element_by_xpath('//a[@href="/explore/tabs/trending"]').click()

        #sleep(3)
        postnum = 0
        postnum+=4
        #self.driver.find_element_by_css_selector("#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div.css-1dbjc4n.r-1jgb5lz.r-1ye8kvj.r-13qz1uu > div > div > section > div > div > div:nth-child({0}) > div >  div > div > div:nth-child(2) > span".format(postnum)).click()
        
        keyword = KEY
        self.driver.get('https://twitter.com/search?q=%23' + keyword + '&src=typed_query')
        sleep(5)
        
        sleep(1)
        scroll_attempt = [0]


        data = []
        tweet_ids = set()
        last_position = self.driver.execute_script("return window.pageYOffset;")
        scrolling = True

        for i in range(3):
            page_cards = self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
            for card in page_cards:
                tweet = self.get_tweet_data(card)
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)

            scroll_attempt = 0
            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(1)
                curr_position = self.driver.execute_script("return window.pageYOffset;")
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

        self.driver.close()
        sleep(5)

        
    #Get top usersers on Twitter
    def get_toptweet_data(self,card, i): 
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

    def topusers(self): 
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
                    tweet = self.get_toptweet_data(card, i)
                    top_data.append(tweet)
                except NoSuchElementException:
                    i+=1
                    tweet = self.get_toptweet_data(card, i)
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

instance = Twitter_Scrape('fau')

