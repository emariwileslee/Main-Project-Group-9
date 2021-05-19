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
from network.Instascrape import InstaScrape
from network.TweetScrape import TweetScrape
from network.trend_node import node
from network.trend_node import nodeClassifier
sys.path.append(".\TCI\.")
#from Trend_Connection_Identifier import TCI
#print("Program Started 69")


class MT_Mapper():
    def __init__(self,root_driver,node_database):
        self.driver = root_driver
        global root_profile
        global output_location
        global node_db
        node_db = node_database
        self.start = time.time()
        self.MAX_LOAD = 150
        #username = "snackertestunit00"
        #password = "Ca4SraTX3pvYuw8"
        self.root_profile = node_db.node_list[0].username#"sgatfau"#"fauorientation"
        self.url = "https://www.instagram.com/"+self.root_profile+"/"#"https://www.instagram.com/explore/tags/als/"
        #redirect_url = "https://www.instagram.com/fauhousing/live/"
        self.output_location = r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Mapper\Output'#r'C:\Users\emari\Documents\Engineering Design 1\Trend Network Mapper Prototype\Web Scraping\Scrapped Content'
        node_db.output_location = self.output_location
        root_profile = self.root_profile
        output_location = self.output_location
        #KEYWORD = ["FAU","Owls"]
        self.START_THREADS = threading.active_count()
        self.MAX_THREADS = 3#Starts at 0, Must be at least 1
        self.MAX_THREADS += 1
        self.OPERATION_MODE = True #True is Mapper || False is Post Collector
        self.PLATFORM_MODE = True #True is Instagram || False is Twitter
        self.exit_flag = False
        global initialEvent
        initialEvent = threading.Event()
        self.threadArray = np.empty((self.MAX_THREADS+2,),dtype=object)

    def threadInitialize(self):
        self.threadArray[0] = myThreads(0,"Thread-0",0,self.url,initialEvent,self.MAX_LOAD,self.MAX_THREADS,self.PLATFORM_MODE,self.OPERATION_MODE,self.driver)
        self.threadArray[0].start()
        print("Thread 0 Started")
        for i in range(1,self.MAX_THREADS):
            #print("I got here")
            initialEvent.wait()
            self.threadArray[i] = myThreads(i,"Thread-%d"%i,i,self.url,initialEvent,self.MAX_LOAD,self.MAX_THREADS,self.PLATFORM_MODE,self.OPERATION_MODE)
            print("Creating ", self.threadArray[i].name)
            #print("Initial thread complete")
            self.threadArray[i].start()
            #print("ACTIVE THREADS CURRENTLY: ",threadArray[i].active_count())
            #threadArray[i].join()
    
    def exportNodeDB(self):
        return node_db
    
    def exitThread(self):
        global node_db
        while not self.exit_flag:
            if not threading.active_count()>self.START_THREADS:
                self.exit_flag = True
                self.threadArray[self.MAX_THREADS+1] = myThreads(self.MAX_THREADS+1,"Final Thread",self.MAX_THREADS+1,self.url,initialEvent,self.PLATFORM_MODE,self.OPERATION_MODE)
                self.threadArray[self.MAX_THREADS+1].printGlobalinitialUserList()
                end = time.time()
                print("Execution Time: ",end-self.start, " seconds")
                try:
                  node_db.exportNetwork()
                except:
                  print('Write Error, Unable to export trend network')
                  pass
                return node_db
       
class myThreads(threading.Thread):
   def __init__(self, threadID, name, counter, url, event, MAX_LOAD, MAX_THREADS,plat_flag=True,op_type=True,root_driver=None):
      global root_profile
      global output_location
      #print("Thread Initialized")
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.root_driver = root_driver
      self.operation_flag = op_type
      self.platform_flag = plat_flag
      self.name = name
      self.counter = counter
      self.url = url
      self.parent_node = root_profile
      self.current_load = 0
      self.MAX_LOAD = MAX_LOAD
      self.MAX_THREADS = MAX_THREADS
      self.account_cycle = 1
      #self.currentLoad = 0
      if plat_flag == True:
          self.ROWS = 2
      else:
          self.ROWS = 3
      self.COLUMNS = 1
      self.KEYWORD = ["Armenia","Armenian","Armenian Genocide","armeniangenocide","#armeniangenocide","turkeyfailed","genocide","ottoman","turk","turkey","1915","#1915","artsakh"]#["FAU","Orienation","Owls","Boca","Florida","Atlantic","University","#fau"] 
      self.event_obj = event
      #self.startFlag = self.event_obj.wait()
      self.username = ['snackertest99','ewcatlan','jssnackmore','sablernat','jcsnaccFAU','snackertestunit00','worilber',]#'ewltest99'#"jksnacker00"#"snackertestunit00"#'jksnacker00'
      self.password = ['KC^&0ecp%8%o','mfW!bcX0#*o5','Uf8w#Cy6jm4B','I03lYJUL&TD&','BaiK16*0spB$','Ca4SraTX3pvYuw8','Uka^CxqusZmW',]#"ESctQtHDKxa56we"#'ESctQtHDKxa56we'
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
      global num_of_nodes
      threadQueue=1
      num_of_nodes = len(node_db.node_list)
      #tci_inst = TCI()
      print("****GOOGLE WORD2VEC DATABASE LOAD COMPLETE****")
      initialUserList = [np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object)]
      currentLoad = []
      #node_db = nodeClassifier(output_location)
      print("Starting "+self.name)
      if self.operation_flag == True and self.platform_flag == True:
          instance = InstaScrape(node_db.node_list[0].root_post_url,self.root_driver)
      elif self.operation_flag == True and self.platform_flag == False:
          instance = TweetScrape(self.url)
      else:
          pass

      if self.root_driver is not None:
          pass
      else:
          instance.login(self.username[0],self.password[0])
          instance.seedSelect()
      #Instagram Specific
      #self.parent_node = root_profile
      bufferNode = node()
      #root_node = root_profile
      for k in range(len(node_db.node_list)):
          #print('i GOT HERE')
          #if node_db.node_list[k].connection_type == 'ROOT':
          bufferNode = instance.postGrab(self.KEYWORD,node_db.node_list[k].root_post_url)# ROWS, COLUMNS
          try:
              node_db.node_list[k].child_connections = bufferNode.child_connections
          except:
              pass
          '''else:
              bufferNode = instance.page_nav(self.ROWS,self.COLUMNS,self.KEYWORD)# ROWS, COLUMNS
              node_db.node_list[k].child_connections = bufferNode.child_connections'''
      #bufferNode.parent_node = self.parent_node
      #bufferNode.username = root_profile
      #bufferNode.connection_type = 'ROOT'
      #node_db.addNode(bufferNode)      
      
      #print(np.asarray(initialUserList).shape)
      for i in range(len(node_db.node_list)):
              print(node_db.node_list[0].child_connections[i])
      for k in range(len(node_db.node_list)):    
          for i in range(len(node_db.node_list[k].child_connections)):  
              currentLoad.append(floor(len(node_db.node_list[k].child_connections[i]) / 3))#CHANGE THIS 6 TO ADUST LOAD FOR RIGHT NOW
      #instance.Insta_User_Branching(3,1,KEYWORD)# ROWS, COLUMNS
      
      #sleep(5)
      try:
          node_db.exportNetwork()
      except:
          print('Write Error, Unable to export trend network')
          pass
      
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
      global gl_cycle_counter
      global num_of_nodes
      threadCounter = 0
      gl_cycle_counter = 1
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
      if self.operation_flag == True and self.platform_flag == True:
          currentURL = "https://www.instagram.com/"+node_db.node_list[0].child_connections[1][index[1]]+"/"#REMEMBER TO CHANGE THIS LATER
          instance = InstaScrape(currentURL)
      elif self.operation_flag == True and self.platform_flag == False:
          currentURL = "https://www.twitter.com/"+node_db.node_list[0].child_connections[1][index[1]]+"/"#REMEMBER TO CHANGE THIS LATER
          instance = TweetScrape(currentURL)
      else:
          pass
      instance.login(self.username[(self.threadID-1)],self.password[(self.threadID-1)])
      instance.seedSelect()
      #THIS IS THE ACTUAL PATHING SECTION OF THE CODE
      for k in range(0,len(node_db.node_list)):
          for lists in range(1,len(node_db.node_list[k].child_connections)):
              self.MapperNodeCollection(instance, node_db.node_list[0].child_connections,index, lists)
          if threading.active_count()<9:
              break
      
      print("Layer 1 Connections Complete in Thread {0}".format(self.threadID))
      threadQueue+=1
      threadCounter=0
      while(threadQueue<3 or threading.active_count()>8):
          pass
      '''if threadCounter<1:
          threadCounter+=3
          for i in range(2,len(node_db.node_list)):
              for k in range(len(node_db.node_list[i].child_connections[1])):
                  bufferNode = node()
                  bufferNode.parent_node = node_db.node_list[i].username
                  bufferNode.username = node_db.node_list[i].child_connections[1][k]
                  bufferNode.connection_type = 'like'
                  node_db.addNode(bufferNode)
          node_db.exportNetwork()
          threadCounter+=2'''
      if threadCounter>=3:
          #threadQueue=0
          #threadCounter=0
          threadQueue=0    
      
      print("ALL THREADS COMPLETE\n ")
      
      list_length = range(0,len(node_db.node_list))
      #length_buffer = len(node_db.node_list)
      try:
          node_db.exportNetwork()
      except:
          print('Write Error, Unable to export trend network')
          pass
      cycle_counter = 2
      gl_cycle_counter+=1
      #print("Size of child connections: ",len(node_db.node_list[0].child_connections[1]))
      threadCounter=0
      #driver_check = []
      bufferList = []
      for i in list_length:
          bufferList.append(node_db.node_list[i].child_connections[1])
      print(bufferList)
      
      for lists in range(list_length):
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
          
          self.MapperNodeCollection(instance, node_db.node_list[lists].child_connections,index, 1)
          try:
              node_db.exportNetwork()
          except:
              print('Write Error, Unable to export trend network')
              pass
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
              while(threadQueue<3):#DONT DO THIS VERY BAD BUSY WAIT !!! 
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
            
      try:
          node_db.exportNetwork()
      except:
          print('Write Error, Unable to export trend network')
          pass
      print("Exiting ", self.name)
      instance.teardown_method()
      #instance.teardown_method()
      #sys.exit()
   
   def MapperNodeCollection(self,driver_instance, username_list,index,lists):
       global tci_inst
       global node_db
       global num_of_nodes
       bufferNode = node()
       
       #print("I got here, ThreadID: {0}".format(self.threadID))
       if self.threadID==1:#and gl_cycle_counter==1:
              for i in username_list[lists][0:currentLoad[lists]]:
                  if(self.current_load>=self.MAX_LOAD and self.account_cycle<2):
                       driver_instance.logout()
                       driver_instance.login(self.username[(self.threadID-1)+(self.MAX_THREADS*self.account_cycle)],self.password[(self.threadID-1)+(self.MAX_THREADS*self.account_cycle)])
                       self.account_cycle+=1
                       self.current_load = 0
                  else:
                      pass
                  self.current_load+=1
                  print("Thread: {0}  Load:{1}".format(self.threadID,self.current_load))
                  if self.operation_flag == True and self.platform_flag == True:
                      currentURL = "https://www.instagram.com/"+i+"/"
                      driver_instance.userRedirect(currentURL)
                  elif self.operation_flag == True and self.platform_flag == False:
                      currentURL = "https://www.twitter.com/"+i+"/"
                      driver_instance.userRedirect(currentURL)
                  if self.operation_flag == True and self.platform_flag == True:
                      bufferNode = driver_instance.page_nav(self.ROWS,self.COLUMNS, self.KEYWORD)
                  elif self.operation_flag == True and self.platform_flag == False:
                      bufferNode = driver_instance.page_nav(self.ROWS, self.KEYWORD)
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
                      node_db.exportNetwork()
                      #for i in range(len(bufferNode.captions)):
                          #tci_inst.addSample(bufferNode.captions[i])
                  else:
                      pass
                  
       else:
              for i in username_list[lists][index[lists]:(index[lists]*2)]:#CHECK OUT THIS LINE MAYBE BUG !!!
                  #print("I got here too2, ThreadID: {0}".format(self.threadID))
                  #print(i)
                  #node_db.addNode(root_node, i,'unknown')
                  if(self.current_load>=self.MAX_LOAD and self.account_cycle<3):
                       driver_instance.logout()
                       driver_instance.login(self.username[(self.threadID-1)+(self.MAX_THREADS*self.account_cycle)],self.password[(self.threadID-1)+(self.MAX_THREADS*self.account_cycle)])
                       self.account_cycle+=1
                       self.current_load = 0
                  else:
                      pass
                  self.current_load+=1
                  print("Thread: {0}  Load:{1}".format(self.threadID,self.current_load))
                  if self.operation_flag == True and self.platform_flag == True:
                      currentURL = "https://www.instagram.com/"+i+"/"
                      driver_instance.userRedirect(currentURL)
                  elif self.operation_flag == True and self.platform_flag == False:
                      currentURL = "https://www.twitter.com/"+i+"/"
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
                      dupe_flag = False    
                      for j in range(len(node_db.node_list)):
                          if node_db.node_list[j].username == bufferNode.username:
                              dupe_flag = True
                      if dupe_flag != True:
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
       try:
          node_db.exportNetwork()
       except:
          print('Write Error, Unable to export trend network')
          pass
       node_db.printNetwork()
       #tci_inst.sampleSenTrendMean()
       testtext = 'london bridge is falling down in spain with the queen doing a sacred dance on the sun from jupiter'
       print("Initial text data: ",testtext)
       #print("This is the distance of your vector from the initial centroid(SENTENCE-CENTROID): ",tci_inst.distanceCentroid(testtext))
       print("\n\nFinal user network lists: ")
       for i in range(len(node_db.node_list[0].child_connections)):
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
          print(node_db.node_list[0].child_connections[i])
       sys.exit()

#instance = MT_Mapper()

        
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