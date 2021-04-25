# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 09:37:32 2021

@author: emari
"""
import os
import sys
from time import sleep
sys.path.append(".\SNACC_Mapper\.")
from Mapper_Threading import MT_Mapper
from trend_node import nodeClassifier
sys.path.append(".\SNACC_Post_Collector\.")
from Instagram_Scraper import Instagram_Scraper
#Other code and steps go here

global node_db
output_location_main = r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Mapper\Output'

node_db = nodeClassifier(output_location_main)
post_collector = Instagram_Scraper()
node_db = post_collector.exportNodeDB()
node_db.output_location = output_location_main
node_db.exportNetwork()
root_driver = post_collector.exportRootDriver()
mapper = MT_Mapper(root_driver,node_db)
mapper.threadInitialize()
node_db = mapper.exportNodeDB()
while mapper.exit_flag == False:
    sleep(30)
    try:
          node_db.exportNetwork()
    except:
          print('Write Error, Unable to export trend network')
          pass

'''try:
    os.startfile('.\SNACC_Visual\demo.html')#Starts the visualizer menu
except:
    print('Could not start SNACC Visualizer')'''
