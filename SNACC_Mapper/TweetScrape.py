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
           element_present = EC.presence_of_element_located((By.NAME,"session[username_or_email]"))
           WebDriverWait(self.driver,10).until(element_present)
           if self.driver.find_element(By.NAME, "session[username_or_email]"):
                sleep(1)#AFTER PROTOTYPING USE WEB WAIT FOR SLEEP
                self.driver.find_element(By.NAME, "session[username_or_email]").click()
                # 7 | type | name=username |
                self.driver.find_element(By.NAME, "session[username_or_email]").send_keys(USERNAME) #USERNAME
                # 8 | click | name=password |  | 
                self.driver.find_element(By.NAME, "session[password]").click()
                # 9 | type | name=password |
                self.driver.find_element(By.NAME, "session[password]").send_keys(PASSWORD) #PASSWORD
                # 10 Click login button on the sign in page
                self.driver.find_element(By.CSS_SELECTOR, "div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(8) > div").click()
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(8) > div"))).click()
                except:
                    pass
                    '''try:
                        self.login(USERNAME, PASSWORD)
                    except:
                        print("Could not complete login")'''
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
                    pass
                    '''try:
                        self.login(USERNAME, PASSWORD)
                    except:
                        print("Could not complete login")'''
       
        def logout(self):#This is used to log out of a user account
            #This clicks the profile menu
            self.driver.find_element(By.CSS_SELECTOR, ".qNELH > .\\_6q-tv").click()
            #This clicks the logout button
            self.driver.find_element(By.XPATH, "//div[2]/div[2]/div/div/div/div/div/div/div").click() 
       
        def page_nav(self,ROWS,KEYWORD):# This is used to navigate to individual posts on the page
            userNode = node()  
            empty_flag = False
            trend_related_flag = False 
            bio = self.bio_Grab()
            #PATHING CODE HERE
            for row in range(1,ROWS):
                try:
                  for i in range(0,4):
                    page_cards = self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
                    #for card in page_cards:
                    tweet = self.get_tweet_data(page_cards[i])
                    self.driver.find_element_by_xpath(page_cards[i]).click()
                except:
                    #print("Grid Structure Not Found")
                    empty_flag = True
                    pass
                
                if self.trendConnectionID(bio,KEYWORD) == True  and empty_flag == False:#or self.trendConnectionID(self.comment_Grab(),KEYWORD) == True'''
                    sleep(0.5)
                    trend_related_flag = True
                    likes_buffer = self.likes_grab()
                    if(likes_buffer==0):
                        print("Above Likes Threshold !!!")
                        trend_related_flag = False
                    userNode.total_likes+=likes_buffer
                    userNode.parent_node = "user"
                    try:
                        userNode.captions.append(self.comment_Grab())
                    except:
                        pass
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div.css-1dbjc4n.r-aqfbo4.r-kemksi.r-1igl3o0.r-rull8r.r-qklmqi.r-gtdqiz.r-1gn8etr.r-1g40b8q > div.css-1dbjc4n.r-1loqt21.r-136ojw6 > div > div > div > div > div.css-1dbjc4n.r-1habvwh.r-1pz39u2.r-1777fci.r-15ysp7h.r-s8bhmr > div").click()#Close post
                except:
                    pass
            if trend_related_flag == True:
                userNode.child_connections[0] = np.append(userNode.child_connections[0],np.asarray(self.returnUsernameList()))
                userNode.child_connections[1] = np.append(userNode.child_connections[1],np.asarray(self.returnLikesList()))
                userNode.child_connections[2] = np.append(userNode.child_connections[2],np.asarray(self.returnCommentList()))
                userNode.child_connections[3] = np.append(userNode.child_connections[3],np.asarray(self.returnFollowerList()))
                userNode.child_connections[4] = np.append(userNode.child_connections[4],np.asarray(self.returnFollowingList()))
                return userNode
            else:
                return False
        
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
            #node_db.addNode(bufferNode)
            return bufferNode
        
        def likes_grab(self):#Navigate to post then call this function after
            try:
                try:
                    likeNumstr = self.driver.find_element(By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(4) > div > div:nth-child(3) > div > a > div > span > span").text #CHANGE 'a' to 'button' IF STOPS WORKING
                    if 'K' in likeNumstr:
                        like_buffer = likeNumstr
                        like_buffer = like_buffer.replace('K','')
                        like_buffer = like_buffer.split('.')
                        print(like_buffer)
                        try:
                            like_int = like_buffer[0] + like_buffer[1]+'00'
                        except:
                            like_int = like_buffer[0] + '000'
                            
                except:
                    likeNumstr = self.driver.find_element(By.CSS_SELECTOR, "div.Nm9Fw:nth-child(1) > button:nth-child(1) > span:nth-child(1)").text
                if likeNumstr.find(",") != -1:
                    likeNumstr = likeNumstr.replace(',','')
                likeNum = int(likeNumstr)
                if likeNum > 150:#FOR DEMONSTRATION, TAKE OUT OF PRODUCTION CODE
                    return 0
                    pass
                else:
                    #print("Number of likes : ", likeNum)
                    self.driver.find_element(By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(4) > div > div:nth-child(3) > div > a").click()#Open likes #CHANGE 'a' to 'button' IF STOPS WORKING
                    sleep(2)
                    source = ""
                    userList = []
                    cycleNum = ceil((10*likeNum) / 36) + 1 #Number of Cycles addition +1 cycle is performed for accuracy
                    #currentUser = 11
                    for x in range(cycleNum):
                        self.likes_scroll(self,10)#Set to 48 for subsequent total list transversal
                        sleep(0.1)
                        #print("CYCLE: ",x+1)
                
                        for i in range(1,20):
                            try:
                                source = self.driver.find_element(By.CSS_SELECTOR,"div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv > div:nth-child(2) > div >div:nth-child(2) > div > div > section > div > div > div:nth-child({0}) > div > div > div > div:nth-child(2) > div > div > a > div > div:nth-child(2) > div > span".format(i)).text
                                source = source.replace('@','')
                            except: #NoSuchElementException:
                                pass
                            if((source in userList)==False):
                                userList.append(source)
                                
                   
                    '''print("START OF ARRAY PRINT")
                    for i in userList:
                        print(i) '''
                        
                    #print("userList Final Size: ",len(userList))
                    self.driver.find_element(By.CSS_SELECTOR, "body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button").click()#Close likes
                    sleep(0.5)
                    #self.driver.find_element(By.CSS_SELECTOR, "div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button:nth-child(1)").click()#Close post
                    for i in userList:
                        if((i in self.allUserList)==False):#Ensures only new usernames are recorded, no repeats
                            self.allUserList.append(i)
                            self.likes_List.append(i)
                    return like_int    
            except: #NoSuchElementException:
                #print("No likes found")
                return 0
                #self.driver.find_element(By.CSS_SELECTOR, "body > div._2dDPU.CkGkG > div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button").click()#Close post
  
        def likes_scroll(self,N_Tab): #N_Tab is number of times to press, set to 66 for total list transversal
            element = self.driver.find_element(By.CSS_SELECTOR, "#layers > div:nth-child(2) > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-1867qdf.r-1wbh5a2.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1.r-htvplk.r-1udh08x > div > div.css-1dbjc4n.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-1ye8kvj.r-13qz1uu > div")
            actions = ActionChains(self.driver)
            #actions.reset_actions()
            #actions.move_to_element(element).perform()
            for i in range(N_Tab):
                actions.send_keys(Keys.TAB)
                
            actions.perform()    
            self.driver.execute_script("arguments[0].scrollIntoView();",element) 
       
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
       
        def caption_Grab(self):
          try:
              firstComment = self.driver.find_element(By.CSS_SELECTOR,"#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(1) > div > div > span").text
              #print(firstComment)
              return firstComment
          except:
              pass 
       
        def bio_Grab(self):
          try:
              bio = self.driver.find_element(By.CSS_SELECTOR,"#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(3) > div > div > span").text
              #print(firstComment)
              return bio
          except:
              pass
        
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
        def userRedirect(self,name):
           self.driver.get('https://twitter.com/search?q=%40{0}&src=typed_query'.format(name))
           #self.driver.find_element_by_css_selector('#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-aqfbo4.r-zso239.r-1hycxz > div > div.css-1dbjc4n.r-1xcajam.r-ipm5af.r-1hycxz > div > div > div > div.css-1dbjc4n.r-1awozwy.r-aqfbo4.r-kemksi.r-18u37iz.r-1h3ijdo.r-6gpygo.r-15ysp7h.r-1xcajam.r-ipm5af.r-1hycxz.r-136ojw6 > div > div > div > form > div.css-1dbjc4n.r-1wbh5a2 > div > div > div.css-901oao.r-1fmj7o5.r-6koalj.r-16y2uox.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0 > input').click()
           #self.driver.find_element_by_css_selector('#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-aqfbo4.r-zso239.r-1hycxz > div > div.css-1dbjc4n.r-1xcajam.r-ipm5af.r-1hycxz > div > div > div > div.css-1dbjc4n.r-1awozwy.r-aqfbo4.r-kemksi.r-18u37iz.r-1h3ijdo.r-6gpygo.r-15ysp7h.r-1xcajam.r-ipm5af.r-1hycxz.r-136ojw6 > div > div > div > form > div.css-1dbjc4n.r-1wbh5a2 > div > div > div.css-901oao.r-1fmj7o5.r-6koalj.r-16y2uox.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0 > input').send_keys(name)
           sleep(3)
           self.driver.find_element_by_css_selector('#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > div > section > div > div > div:nth-child(3) > div > div > div > div.css-1dbjc4n.r-1iusvr4.r-16y2uox > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wtj0ep > div.css-1dbjc4n.r-1wbh5a2.r-dnmrzs > a > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-dnmrzs > div.css-901oao.css-bfa6kz.r-1fmj7o5.r-1qd0xha.r-a023e6.r-b88u0q.r-rjixqe.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0 > span > span').click()
           #actions = ActionChains(self.driver)
           #actions.send_keys(Keys.ENTER)
'''initial_url = 'https://twitter.com/FAUBaseball'           
instance = TweetScrape(initial_url)
instance.login('JKarnol','^2pNVT%ttzuoX')
instance.userRedirect('FAUBaseball')
instance.page_nav(4,'owls')'''

#CARD HTML
#div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > div:nth-child(3) > section > div > div > div:nth-child({0}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz
#ALTERNATE
##react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > div:nth-child(3) > section > div > div > div:nth-child({0})

#Likes
##react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(4) > div > div:nth-child(2) > div > a
#Likes Num
#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(4) > div > div:nth-child(3) > div > a > div > span > span

#Retweets
##react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div:nth-child(3) > div:nth-child(4) > div > div.css-1dbjc4n.r-1mf7evn > div > a

#Back Button
##react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-kemksi.r-1kqtdi0.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div.css-1dbjc4n.r-aqfbo4.r-kemksi.r-1igl3o0.r-rull8r.r-qklmqi.r-gtdqiz.r-1gn8etr.r-1g40b8q > div.css-1dbjc4n.r-1loqt21.r-136ojw6 > div > div > div > div > div.css-1dbjc4n.r-1habvwh.r-1pz39u2.r-1777fci.r-15ysp7h.r-s8bhmr > div > div