#!/usr/bin/env python
# coding: utf-8

# In[12]:


import re
import csv
import emoji
import string
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

import os
import wget
import sys
sys.path.append("..\SNACC_Mapper\.")
from trend_node import node
from trend_node import nodeClassifier

#global node_db 
#node_db = nodeClassifier(r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Post_Collector')

class Instagram_Scraper():
    def __init__(self):
        self.node_db = nodeClassifier(r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Post_Collector')
        self.img_url_list = []
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #self.get_post_data()
        self.login()
        self.navigate()
        self.node_db.exportNetwork()
        #self.getimages()
        
    def get_post_data(self,card):
        bufferNode = node()
        bufferNode.root_post_url = self.driver.current_url
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a"))).text#card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a").text
        bufferNode.username = username
        bufferNode.parent_node = username
        bufferNode.connection_type = 'ROOT'
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        caption = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span").text
        bufferNode.captions.append(caption)
        result = 0
        try:
            like_count = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span").text#card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a").text
            result = like_count
            if ',' in result:
                result = result.replace(',','')
                #result = result.split(' ')
            bufferNode.total_likes+=int(result)

        except NoSuchElementException:
            try:
                view_count = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span").text
                pass
            except NoSuchElementException:
                first_like = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div").text
                pass

        post = (username, caption, result, postdate)
        self.node_db.addNode(bufferNode)
        return post

    
    def login(self):
        
        #open the webpage
        self.driver.get("http://www.instagram.com")
        sleep(1)

        #Username
        username = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        username.clear()
        username.send_keys('SNACC_FAU')

        #passwordHardcodedForFullAutomation
        password = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.clear()
        password.send_keys('1password1')
        password.send_keys(Keys.RETURN)
        sleep(2)

    def navigate(self):
        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        not_now2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        sleep(2)
        keyword = 'fau'
        self.driver.get('https://www.instagram.com/explore/tags/{0}/'.format(keyword))
        #Search
        '''searchbox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        searchbox.clear()
        keyword = "#fau"
        searchbox.send_keys(keyword)
        time.sleep(5)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)
        #doesnt always send have to click twice
        searchbox.send_keys(Keys.ENTER)''' 
        #time.sleep()
        try:
            search_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Nnq7C:nth-child(1) > div:nth-child(1) > a:nth-child(1)"))).click()
        except NoSuchElementException:
            search_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Nnq7C:nth-child(1) > div:nth-child(1) > a:nth-child(1)"))).click()
        sleep(3)

        data = []

        for n in range(1):#CHANGE THIS FOR ROWS
            page_cards = self.driver.find_elements_by_xpath('//div[@role="dialog"]')
            for card in page_cards:
                post = self.get_post_data(card)
                data.append(post)
                time.sleep(2)
                click_next = self.driver.find_element_by_css_selector("body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow").click()
                #time.sleep(2)
        #print(data)

        #sleep(5)
        #put into CSV
        with open('IS_op.csv', 'w', newline='', encoding='utf-8') as f:
            header = ['UserName', 'Caption', 'Likes/Views', 'PostDate']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

        self.driver.get('https://www.instagram.com/explore/tags/{0}/'.format(keyword))
        #sleep(5)
        
    def exportNodeDB(self):
        return self.node_db
    
    def exportRootDriver(self):
        return self.driver
    
    def getimages(self):
        #navigate back to main page
        search_input = self.driver.find_element_by_xpath("/html/body/div[5]/div[3]/button").click()

        #get all images 
        self.driver.execute_script("window.scrollTo(0,4000);")

        images = self.driver.find_elements_by_tag_name('img')
        images = [image.get_attribute('src') for image in images]

        images

        path = os.getcwd()
        #path = os.path.join(path, keyword[1:] + "s")

        os.mkdir(path)
        path

        counter = 0
        for image in images:
            #save_as = os.path.join(path, keyword[1:] + str(counter) + '.jpg')
            #wget.download(image, save_as)
            counter += 1
   
            
#instance = Instagram_Scraper()


# In[ ]:




