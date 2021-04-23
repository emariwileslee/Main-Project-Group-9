# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 17:21:29 2021

@author: emari
"""
import pandas as pd
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

class account():
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email_address = ""

class botGenerator():
    def __init__(self,output_location):
        self.primary_email = 'jksnackerbox'
        self.output_location = output_location
        self.account_df = pd.DataFrame(columns=["username","password","email_address"])
    
    def accountCreation(self):
        bufferAccount = account()
        bufferNum = np.random.randint(0,10000)
        buffUser = self.primary_email+str(bufferNum)+'@gmail.com'
    def emptyInbox(self):
        pass
    
    def exportDF(self):
        self.account_df.to_csv(self.output_location+"\output.csv",index=False)
    