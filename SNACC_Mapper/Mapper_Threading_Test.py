# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:11:25 2021

@author: emari
"""
import pandas as pd
import numpy as np
import sys
import threading
import time
from math import floor
sys.path.append(".")
from Instascrape import InstaScrape
from trend_node import node
from trend_node import nodeClassifier
sys.path.append(".\TCI\.")
from Trend_Connection_Identifier import TCI

       
class myThreads(threading.Thread):
   def __init__(self, threadID, name, counter, url, event):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.url = url
      #self.currentLoad = 0
      self.ROWS = 1
      self.COLUMNS = 1
      self.KEYWORD = ["FAU","Orienation","Owls","Boca"]
      self.event_obj = event
      #self.startFlag = self.event_obj.wait()
      self.username = "ewltest99"
      self.password = "Ca4SraTX3pvYuw8"
      print("ACTIVE THREADS CURRENTLY: ", threading.active_count())
    
   def run(self):
      if(self.threadID==0):
          self.mainThread()
      else: 
          self.childThread()
          
   def mainThread(self):
      global initialUserList
      global currentLoad
      global root_node
      global node_db
      global tci_inst
      global threadQueue
      threadQueue+=1
      tci_inst = TCI()
      print("****GOOGLE WORD2VEC DATABASE LOAD COMPLETE****")
      initialUserList = [np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object)]
      currentLoad = []
      node_db = nodeClassifier(output_location)
      print("Starting "+self.name)
      instance = InstaScrape(self.url)
      instance.login(username,password)
      instance.seedSelect()
      
      root_node = root_profile
      instance.page_nav(self.ROWS,self.COLUMNS,self.KEYWORD)# ROWS, COLUMNS
      initialUserList[0] = np.append(initialUserList[0],np.asarray(instance.returnUsernameList()))
      initialUserList[1] = np.append(initialUserList[1],np.asarray(instance.returnLikesList()))
      initialUserList[2] = np.append(initialUserList[2],np.asarray(instance.returnCommentList()))#USED TO TEST SYSTEM CHANGE BACK TO COMMENT
      initialUserList[3] = np.append(initialUserList[3],np.asarray(instance.returnFollowerList()))
      initialUserList[4] = np.append(initialUserList[4],np.asarray(instance.returnFollowingList()))
      
      print(np.asarray(initialUserList).shape)
      for i in range(5):
          print(initialUserList[i])
      
      for i in range(len(initialUserList)):  
          currentLoad.append(floor(len(initialUserList[i]) / 3))#CHANGE THIS 6 TO ADUST LOAD FOR RIGHT NOW
      #instance.Insta_User_Branching(3,1,KEYWORD)# ROWS, COLUMNS
      
      #sleep(5)
      print("Exiting ", self.name)
      instance.teardown_method()
      threadQueue-=1
      self.event_obj.set()
      
      #self.event_obj.clear()
      #sys.exit()
      
   def childThread(self):
      global node_db
      global initialUserList
      global currentLoad
      global root_node
      global tci_inst
      global threadQueue
      
      index = []
      for i in range(len(currentLoad)):
          index.append(((self.threadID-1) * currentLoad[i]))
      #bufferNode = node()
      print("Starting "+self.name)
      #print(initialUserList)
      if self.threadID==1:
          #index+=1
          print("This is index", index)
          print("This is current load", currentLoad)
      currentURL = "https://www.instagram.com/"+initialUserList[1][index[1]]+"/"
      instance = InstaScrape(currentURL)
      instance.login(username,password)
      instance.seedSelect()
      #THIS IS THE ACTUAL PATHING SECTION OF THE CODE
      for lists in range(1,len(initialUserList)):
          self.InstagramNodeCollection(instance, initialUserList,index, lists)
      
      print("Layer 1 Connections Complete in Thread {0}".format(self.threadID))
      threadQueue+=1
      while(threadQueue<3):
          pass
      threadQueue=0
      print("ALL THREADS COMPLETE")
      
      list_length = len(node_db.node_list)
      cycle_counter = 2
      
      for lists in range(1,list_length):
          for i in range(len(node_db.node_list[lists].child_connections)):  
              currentLoad.append(floor(len(node_db.node_list[lists].child_connections[i]) / 3))#CHANGE THIS 6 TO ADUST LOAD FOR RIGHT NOW
          for i in range(len(currentLoad)):
              index.append(((self.threadID-1) * currentLoad[i]))
              print("Thread - {0} - Index: {1}".format(self.threadID,index))
          
          self.InstagramNodeCollection(instance, node_db.node_list[lists].child_connections,index, lists)
          
          
          if lists == list_length-1:
              threadQueue+=1
              while(threadQueue<3):
                  pass
              threadQueue=0
              print("ALL THREADS COMPLETE")
              print("Layer {0} Connections Complete".format(cycle_counter))
              cycle_counter+=1
              list_length = len(node_db.node_list)
            
      
      print("Exiting ", self.name)
      instance.teardown_method()
      #instance.teardown_method()
      #sys.exit()
   
   def InstagramNodeCollection(self,driver_instance, username_list,index,lists):
       global tci_inst
       global node_db
       bufferNode = node()
       if self.threadID==1:
              for i in username_list[lists][0:currentLoad[lists]]:
                  #print(i)
                  #node_db.addNode(root_node, i,'unknown')
                  currentURL = "https://www.instagram.com/"+i+"/"
                  driver_instance.userRedirect(currentURL)
                  bufferNode = driver_instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  if bufferNode != False:
                      bufferNode.parent_node = root_node
                      bufferNode.username = i
                      print('Trend related node found: ',bufferNode.username)
                      if lists == 1:
                          bufferNode.connection_type = 'like'
                      elif lists == 2:
                          bufferNode.connection_type = 'comment'
                      elif lists == 3:
                          bufferNode.connection_type = 'follower'
                      elif lists == 4:
                          bufferNode.connection_type = 'following' 
                      bufferNode.child_connections[0] = np.append(bufferNode.child_connections[0],np.asarray(driver_instance.returnUsernameList()))
                      bufferNode.child_connections[1] = np.append(bufferNode.child_connections[1],np.asarray(driver_instance.returnLikesList()))
                      bufferNode.child_connections[2] = np.append(bufferNode.child_connections[2],np.asarray(driver_instance.returnCommentList()))
                      bufferNode.child_connections[3] = np.append(bufferNode.child_connections[3],np.asarray(driver_instance.returnFollowerList()))
                      bufferNode.child_connections[4] = np.append(bufferNode.child_connections[4],np.asarray(driver_instance.returnFollowingList()))
                      node_db.addNode(bufferNode)
                      for i in range(len(bufferNode.captions)):
                          tci_inst.addSample(bufferNode.captions[i])
                  else:
                      pass
                  
       else:
              for i in username_list[lists][index[lists]:(index[lists]*2)]:
                  #print(i)
                  #node_db.addNode(root_node, i,'unknown')
                  currentURL = "https://www.instagram.com/"+i+"/"
                  driver_instance.userRedirect(currentURL)
                  #instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  bufferNode = driver_instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  if bufferNode != False:
                      bufferNode.parent_node = root_node
                      bufferNode.username = i
                      print('Trend related node found: ',bufferNode.username)
                      if lists == 1:
                          bufferNode.connection_type = 'like'
                      elif lists == 2:
                          bufferNode.connection_type = 'comment'
                      elif lists == 3:
                          bufferNode.connection_type = 'follower'
                      elif lists == 4:
                          bufferNode.connection_type = 'following'    
                      bufferNode.child_connections[0] = np.append(bufferNode.child_connections[0],np.asarray(driver_instance.returnUsernameList()))
                      bufferNode.child_connections[1] = np.append(bufferNode.child_connections[1],np.asarray(driver_instance.returnLikesList()))
                      bufferNode.child_connections[2] = np.append(bufferNode.child_connections[2],np.asarray(driver_instance.returnCommentList()))
                      bufferNode.child_connections[3] = np.append(bufferNode.child_connections[3],np.asarray(driver_instance.returnFollowerList()))
                      bufferNode.child_connections[4] = np.append(bufferNode.child_connections[4],np.asarray(driver_instance.returnFollowingList()))
                      node_db.addNode(bufferNode)
                      for i in range(len(bufferNode.captions)):
                          tci_inst.addSample(bufferNode.captions[i])
                  else:
                      pass
   
   def checkStartFlag(self):
       if self.event_obj.is_set()==True:
           print("Event triggered")
           self.event_obj.set()
           return True
       else:
           print("NO Trigger")
           return False
   def printGlobalinitialUserList(self):
       global initialUserList
       global node_db
       global tci_inst
       node_db.exportNetwork()
       node_db.printNetwork()
       tci_inst.sampleSenTrendMean()
       testtext = 'london bridge is falling down in spain with the queen doing a sacred dance on the sun from jupiter'
       print("Initial text data: ",testtext)
       print("This is the distance of your vector from the initial centroid(SENTENCE-CENTROID): ",tci_inst.distanceCentroid(testtext))
       print("\n\nFinal user network lists: ")
       for i in range(len(initialUserList)):
          if(i==0):
             print("\nTotal List:")
          if(i==1):
             print("\nLikes List:")
          if(i==2):
             print("\nComment List:")
          if(i==3):
             print("\nFollower List:")
          if(i==4):
             print("\nFollowing List:")
          print(initialUserList[i])
       sys.exit()


start = time.time()
username = "ewltest99"
password = "Ca4SraTX3pvYuw8"
root_profile = "sgatfau"#"fauorientation"        
url = "https://www.instagram.com/"+root_profile+"/"#"https://www.instagram.com/explore/tags/als/"
#redirect_url = "https://www.instagram.com/fauhousing/live/"
output_location = r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Mapper\Output'#r'C:\Users\emari\Documents\Engineering Design 1\Trend Network Mapper Prototype\Web Scraping\Scrapped Content'
KEYWORD = ["FAU","Owls"]
START_THREADS = threading.active_count()
MAX_THREADS = 3#Starts at 0, Must be at least 1
MAX_THREADS += 1
exit_flag = False

initialEvent = threading.Event()
threadArray = {}
threadArray[0] = myThreads(0,"Thread-0",0,url,initialEvent)
threadArray[0].start()

for i in range(1,MAX_THREADS):
    initialEvent.wait()
    threadArray[i] = myThreads(i,"Thread-%d"%i,i,url,initialEvent)
    print("Creating ", threadArray[i].name)
    #print("Initial thread complete")
    threadArray[i].start()
    #print("ACTIVE THREADS CURRENTLY: ",threadArray[i].active_count())
    #threadArray[i].join()

while not exit_flag:
    if not threading.active_count()>START_THREADS:
        exit_flag = True
        threadArray[MAX_THREADS+1] = myThreads(MAX_THREADS+1,"Final Thread",MAX_THREADS+1,url,initialEvent)
        threadArray[MAX_THREADS+1].printGlobalinitialUserList()
        end = time.time()
        print("Execution Time: ",end-start, " seconds")
        
#threadArray[MAX_THREADS+1] = myThreads(MAX_THREADS+1,"Final Thread",MAX_THREADS+1,url,initialEvent)
#threadArray[MAX_THREADS+1].printGlobalinitialUserList()


#for i in range(1,6):
    #threadArray[i].start()

#instance.page_nav(3,1,KEYWORD)# ROWS, COLUMNS
#.Insta_User_Branching(3,1,KEYWORD)# ROWS, COLUMNS
  
#instance.totalUsernamePrint()

#instance.teardown_method()'''


#Where comments are stored, change the second <ul> tag to transverse list ... increment from two up
#div.EtaWk > ul:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) 

#Where followers are stored, change the <li> tag to transverse list
#div.PZuss:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)

#Where following is stored, change the <li> tag to transverse list
#div.PZuss:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(2)  > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)

#Where nicknames on likes are stored