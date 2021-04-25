# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 09:58:55 2021

@author: emari
"""
import numpy as np
import pandas as pd

class node():
    def __init__(self):
        self.parent_node = ""
        self.child_connections = [np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object),np.array([],dtype=object)]
        self.username = ""
        self.connection_type = ""
        self.captions = []
        self.total_likes = 0
        self.total_followers = 0
        self.total_following = 0
        self.post_date = ""
        self.root_post_url = ""
    
    def printNode(self):
        print("parent node: ",self.parent_node)
        print("username: ",self.username)
        print("connection_type: ",self.connection_type)
        print("total_likes: ",self.total_likes)
        print("total_followers: ",self.total_followers)
        print("total_following: ",self.total_following)
        
class nodeClassifier():
    def __init__(self,output_location):
        self.node_list = []
        self.output_location = output_location
        self.node_df = pd.DataFrame(columns=["parent_node","username","connection_type"])
        
    def addNode(self,node):#(self,parent_node,username,connection_type):
        #nodeBuffer = [parent_node,username,connection_type]
        nodeBuffer = [node.parent_node,node.username,node.connection_type]
        self.node_df = self.node_df.append(pd.Series(nodeBuffer,index=self.node_df.columns),ignore_index=True)
        self.node_list.append(node)
        #print(self.node_df)
        
    def printNetwork(self):
        print(self.node_df)
     
    def exportNetwork(self):
        self.node_df.to_csv(self.output_location+"\output.csv",index=False)