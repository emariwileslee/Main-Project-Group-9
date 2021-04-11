# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:11:25 2021

@author: emari
"""
#print("Program Started 69")
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
#from Trend_Connection_Identifier import TCI
#print("Program Started 69")
       
class myThreads(threading.Thread):
   def __init__(self, threadID, name, counter, url, event):
      #print("Thread Initialized")
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.url = url
      self.parent_node = root_profile
      #self.currentLoad = 0
      self.ROWS = 2
      self.COLUMNS = 1
      self.KEYWORD = ["FAU","Orienation","Owls","Boca","Florida","Atlantic","University"]
      self.event_obj = event
      #self.startFlag = self.event_obj.wait()
      self.username = "jksnacker00"#'ewltest99'#"jksnacker00"#"snackertestunit00"
      self.password = "Ca4SraTX3pvYuw8"#"ESctQtHDKxa56we"
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
      threadQueue=1
      #tci_inst = TCI()
      print("****GOOGLE WORD2VEC DATABASE LOAD COMPLETE****")
      initialUserList = [np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object)]
      currentLoad = []
      node_db = nodeClassifier(output_location)
      print("Starting "+self.name)
      instance = InstaScrape(self.url)
      instance.login(self.username,self.password)
      instance.seedSelect()
      #Instagram Specific
      #self.parent_node = root_profile
      bufferNode = node()
      #root_node = root_profile
      bufferNode = instance.page_nav(self.ROWS,self.COLUMNS,self.KEYWORD)# ROWS, COLUMNS
      bufferNode.parent_node = self.parent_node
      bufferNode.username = root_profile
      bufferNode.connection_type = 'ROOT'
      node_db.addNode(bufferNode)
      
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
      global threadCounter
      threadCounter = 0
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
      currentURL = "https://www.instagram.com/"+initialUserList[1][index[1]]+"/"#REMEMBER TO CHANGE THIS LATER
      instance = InstaScrape(currentURL)
      instance.login(self.username,self.password)
      instance.seedSelect()
      #THIS IS THE ACTUAL PATHING SECTION OF THE CODE
      for lists in range(1,len(initialUserList)):
          self.InstagramNodeCollection(instance, node_db.node_list[0].child_connections,index, lists)
      
      print("Layer 1 Connections Complete in Thread {0}".format(self.threadID))
      threadQueue+=1
      threadCounter=0
      while(threadQueue<3):
          pass
      threadCounter+=1
      if threadCounter>=3:
          threadQueue=0
          #threadCounter=0
      
      print("ALL THREADS COMPLETE\n ")
      
      list_length = range(0,len(node_db.node_list))
      #length_buffer = len(node_db.node_list)
      cycle_counter = 2
      #print("Size of child connections: ",len(node_db.node_list[0].child_connections[1]))
      threadCounter=0
      #driver_check = []
      bufferList = []
      for i in list_length:
          bufferList.append(node_db.node_list[i].child_connections[1])
      print(bufferList)
      
      for lists in list_length:
          self.parent_node = node_db.node_list[lists].username
          print("Thread: {2} Cycle: {0} Size of child connections: {1}\n".format(lists,len(node_db.node_list[lists].child_connections[1]),self.threadID))
          current_load_buffer = []
          index_buffer = []
          for i in range(1,len(node_db.node_list[lists].child_connections)):
              #print("Current Load Number: ",i)
              current_load_buffer.append(floor(len(node_db.node_list[lists].child_connections[i]) / 3))#CHANGE THIS 6 TO ADUST LOAD FOR RIGHT NOW
              #print("Thread - {0} - Current Load: {1}".format(self.threadID,current_load_buffer))
          currentLoad = current_load_buffer
          for i in range(len(currentLoad)):
              #print("Index Number: ",i)
              index_buffer.append(((self.threadID-1) * currentLoad[i]))
              #print("Thread - {0} - Index: {1}".format(self.threadID,index))
          index = index_buffer
          print("Thread {3}: This is the position in the node_list: {0}\n This is threadQueue: {1}\n This is threadCounter: {2}\n".format(lists,threadQueue,threadCounter,self.threadID))
          
          self.InstagramNodeCollection(instance, node_db.node_list[lists].child_connections,index, lists)
          #print("Instagram Node Collection PASSED !!!")
          threadQueue+=1
          threadCounter = 0
          while(threadQueue<3):
              pass
          threadCounter+=1
          if threadCounter>=3:
              threadQueue=0
          if threadQueue == 0:
              threadCounter = 0
          print("ALL THREADS COMPLETE\n ")
          if lists == len(list_length)-1:
              #length_buffer = len(node_db.node_list)
              threadQueue+=1
              threadCounter=0
              while(threadQueue<3):
                  pass
              threadCounter+=1
              if threadCounter>3:
                  threadQueue=0
              if threadQueue == 0:
                  threadCounter = 0
                  #threadCounter=0
              print("ALL THREADS COMPLETE\n ")
              print("Layer {0} Connections Complete".format(cycle_counter))
              cycle_counter+=1
              list_length = range(0,len(node_db.node_list))
            
      
      print("Exiting ", self.name)
      instance.teardown_method()
      #instance.teardown_method()
      #sys.exit()
   
   def InstagramNodeCollection(self,driver_instance, username_list,index,lists):
       global tci_inst
       global node_db
       bufferNode = node()
       #print("I got here, ThreadID: {0}".format(self.threadID))
       if self.threadID==1:
              for i in username_list[lists][0:currentLoad[lists]]:
                  #print("I got here too1, ThreadID: {0}".format(self.threadID))
                  #print(i)
                  #node_db.addNode(root_node, i,'unknown')
                  currentURL = "https://www.instagram.com/"+i+"/"
                  driver_instance.userRedirect(currentURL)
                  bufferNode = driver_instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  if bufferNode != False:
                      bufferNode.parent_node = self.parent_node
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

                      node_db.addNode(bufferNode)
                      #for i in range(len(bufferNode.captions)):
                          #tci_inst.addSample(bufferNode.captions[i])
                  else:
                      pass
                  
       else:
              for i in username_list[lists][index[lists]:(index[lists]*2)]:
                  #print("I got here too2, ThreadID: {0}".format(self.threadID))
                  #print(i)
                  #node_db.addNode(root_node, i,'unknown')
                  currentURL = "https://www.instagram.com/"+i+"/"
                  driver_instance.userRedirect(currentURL)
                  #instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  bufferNode = driver_instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  if bufferNode != False:
                      bufferNode.parent_node = self.parent_node
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

                      node_db.addNode(bufferNode)
                      #for i in range(len(bufferNode.captions)):
                          #tci_inst.addSample(bufferNode.captions[i])
                  else:
                      pass
       return 0
   
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
       #global tci_inst
       node_db.exportNetwork()
       node_db.printNetwork()
       #tci_inst.sampleSenTrendMean()
       testtext = 'london bridge is falling down in spain with the queen doing a sacred dance on the sun from jupiter'
       print("Initial text data: ",testtext)
       #print("This is the distance of your vector from the initial centroid(SENTENCE-CENTROID): ",tci_inst.distanceCentroid(testtext))
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

#print("Program Started 69")
start = time.time()
#username = "snackertestunit00"
#password = "Ca4SraTX3pvYuw8"
root_profile = "sgatfau"#"fauorientation"
url = "https://www.instagram.com/"+root_profile+"/"#"https://www.instagram.com/explore/tags/als/"
#redirect_url = "https://www.instagram.com/fauhousing/live/"
output_location = r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Mapper\Output'#r'C:\Users\emari\Documents\Engineering Design 1\Trend Network Mapper Prototype\Web Scraping\Scrapped Content'
#KEYWORD = ["FAU","Owls"]
START_THREADS = threading.active_count()
MAX_THREADS = 3#Starts at 0, Must be at least 1
MAX_THREADS += 1
exit_flag = False

initialEvent = threading.Event()
threadArray = np.empty((MAX_THREADS+2,),dtype=object)
threadArray[0] = myThreads(0,"Thread-0",0,url,initialEvent)
threadArray[0].start()
print("Thread 0 Started")
for i in range(1,MAX_THREADS):
    #print("I got here")
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