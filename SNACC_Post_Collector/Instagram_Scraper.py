#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import csv
import emoji
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

global node_db 
node_db = nodeClassifier()

class Instagram_Scraper():
    def __init(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.get_post_data()
    def get_post_data(card):
        bufferNode = node()

        username = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a").text
        bufferNode.username = username
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        caption = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span").text
        bufferNode.captions.append(caption)
        try:
            like_count = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a").text
            result = like_count
            bufferNode.total_likes+=result

        except NoSuchElementException:
            try:
                view_count = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span").text
                pass
            except NoSuchElementException:
                first_like = card.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div").text
                pass

        post = (username, caption, result, postdate)
        node_db.addNode(bufferNode)
        return post

    sleep(3)

    #specify the path to chromedriver.exe (download and save on your computer)
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #open the webpage
    driver.get("http://www.instagram.com")
    sleep(1)

    #Username
    username = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    username.clear()
    username.send_keys('SNACC_FAU')

    #passwordHardcodedForFullAutomation
    password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password.clear()
    password.send_keys('1password1')
    password.send_keys(Keys.RETURN)
    sleep(2)

    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

    #Search
    searchbox = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    searchbox.clear()
    keyword = "#cat"
    searchbox.send_keys(keyword)
    time.sleep(5)

    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    #doesnt always send have to click twice
    searchbox.send_keys(Keys.ENTER) 

    time.sleep(2)

    try:
        search_input = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').click()
    except NoSuchElementException:
        search_input = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a').click()
        
    sleep(3)

    data = []

    for n in range(20):
        page_cards = driver.find_elements_by_xpath('//div[@role="dialog"]')
        for card in page_cards:
            post = get_post_data(card)
            data.append(post)
            time.sleep(2)
            click_next = driver.find_element_by_css_selector("body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow").click()
            time.sleep(2)
    print(data)

    sleep(5)
    #put into CSV
    with open('IS_op.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['UserName', 'Caption', 'Likes/Views', 'PostDate']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


    sleep(5)

    #navigate back to main page
    search_input = driver.find_element_by_xpath("/html/body/div[5]/div[3]/button").click()

    #get all images 
    driver.execute_script("window.scrollTo(0,4000);")

    images = driver.find_elements_by_tag_name('img')
    images = [image.get_attribute('src') for image in images]

    images

    path = os.getcwd()
    path = os.path.join(path, keyword[1:] + "s")

    os.mkdir(path)
    path

    counter = 0
    for image in images:
        save_as = os.path.join(path, keyword[1:] + str(counter) + '.jpg')
        wget.download(image, save_as)
        counter += 1

