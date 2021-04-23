# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 06:52:00 2021

@author: emari
"""

import sys
import string
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from time import sleep
from math import ceil
from nltk.tokenize import word_tokenize
sys.path.append(".")
from trend_node import node

class TweetScrape():
    def __init__(self,URL):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.driver =  webdriver.Chrome(ChromeDriverManager().install())#,options=self.chrome_options)
        self.driver.get(URL)
        self.allUserList = []
        self.allUnifiedList = []
        self.likes_List = []
        self.comment_List = []
        self.follower_List = []
        self.following_List = []
        
        self.seed = URL
        #self.allCommentList = []
        self.currDate = datetime.now()
        #self.driver.maximize_window()
    
    def login(self,USERNAME,PASSWORD):#This is used to sign into instagram with a user account to allow greater viewing privelege
       self.driver.get("https://twitter.com/login")
       sleep(1)
       element_present = EC.presence_of_element_located((By.NAME,"username"))
       WebDriverWait(self.driver,10).until(element_present)
       if self.driver.find_element(By.NAME, "username"):
            sleep(1)#AFTER PROTOTYPING USE WEB WAIT FOR SLEEP
            self.driver.find_element(By.NAME, "username").click()
            # 7 | type | name=username |
            self.driver.find_element(By.NAME, "username").send_keys(USERNAME) #USERNAME
            # 8 | click | name=password |  | 
            self.driver.find_element(By.NAME, "password").click()
            # 9 | type | name=password |
            self.driver.find_element(By.NAME, "password").send_keys(PASSWORD) #PASSWORD
            # 10 Click login button on the sign in page
            self.driver.find_element(By.CSS_SELECTOR, "div.css-1dbjc4n.r-eqz5dr.r-1777fci > div > div").click()
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(8) > div"))).click()
            except:
                try:
                    self.login(USERNAME, PASSWORD)
                except:
                    print("Could not complete login")
       else:
            #Selects the login button at the root page
            element = self.driver.find_element(By.CSS_SELECTOR, "#layers > div > div:nth-child(2) > div > div > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wtj0ep.r-rthrr5 > div.css-1dbjc4n.r-1ydw1k6 > div > div:nth-child(1) > a")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            #Selects the center login terminal
            element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions.move_to_element(element).perform()
            # 5 | click | css=.tdiEy > .sqdOP |  | 
            self.driver.find_element(By.CSS_SELECTOR, ".tdiEy > .sqdOP").click()
            # 6 | click | name=username |  | 
            sleep(1)#AFTER PROTOTYPING USE WEB WAIT FOR SLEEP
            self.driver.find_element(By.NAME, "username").click()
            # 7 | type | name=username |
            self.driver.find_element(By.NAME, "username").send_keys(USERNAME) #USERNAME
            # 8 | click | name=password |  | 
            self.driver.find_element(By.NAME, "password").click()
            # 9 | type | name=password |
            self.driver.find_element(By.NAME, "password").send_keys(PASSWORD) #PASSWORD
            # 10 Click login button on the sign in page
            self.driver.find_element(By.CSS_SELECTOR, ".sqdOP > .Igw0E").click()
            # 13 Selects "Not Now" when prompted to save credentials
            #sleep(2)
            #self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button"))).click()
            except:
                try:
                    self.login(USERNAME, PASSWORD)
                except:
                    print("Could not complete login")
       
       def logout(self):#This is used to log out of a user account
            #This clicks the profile menu
            self.driver.find_element(By.CSS_SELECTOR, ".qNELH > .\\_6q-tv").click()
            #This clicks the logout button
            self.driver.find_element(By.XPATH, "//div[2]/div[2]/div/div/div/div/div/div/div").click() 
       
       def page_nav(self,ROWS,COLUMNS,KEYWORD):# This is used to navigate to individual posts on the page
            userNode = node()  
            empty_flag = False
            trend_related_flag = False 
            
            #PATHING CODE HERE
            
            if trend_related_flag == True:
                userNode.child_connections[0] = np.append(userNode.child_connections[0],np.asarray(self.returnUsernameList()))
                userNode.child_connections[1] = np.append(userNode.child_connections[1],np.asarray(self.returnLikesList()))
                userNode.child_connections[2] = np.append(userNode.child_connections[2],np.asarray(self.returnCommentList()))
                userNode.child_connections[3] = np.append(userNode.child_connections[3],np.asarray(self.returnFollowerList()))
                userNode.child_connections[4] = np.append(userNode.child_connections[4],np.asarray(self.returnFollowingList()))
                return userNode
            else:
                return False
       
       def trendConnectionID(self,textData,keyword):
          #print(textData)
          textData = str(textData)
          textData = textData.translate(str.maketrans({key: None for key in string.punctuation}))
          buffer_list = word_tokenize(textData)
          for i in range(len(buffer_list)):
              buffer_list[i] = buffer_list[i].lower()
          #upper = substring.upper()
          for i in range(len(keyword)):
              if keyword[i].lower() in buffer_list:
                  #print("Found",keyword[i])
                  return True
          #print("No keywords found")
          return False
             
       def totalUsernamePrint(self):
        for i in self.allUserList:
            print(i)
        print("Total of All Usernames Collected: ",len(self.allUserList))
      
       def returnUsernameList(self):
          return self.allUserList
       def returnLikesList(self):
          return self.likes_List
       def returnCommentList(self):
          return self.comment_List
       def returnFollowerList(self):
          return self.follower_List
       def returnFollowingList(self):
          return self.following_List 
       
       
       def seedSelect(self):
           currentUrl = self.driver.current_url
           if currentUrl != self.seed :
               self.driver.get(self.seed)
           else:
               pass
       def userRedirect(self,url):
           self.driver.get(url) 