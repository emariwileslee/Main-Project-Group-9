# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 10:13:42 2021

@author: emari
"""

#Using info from : 
#https://towardsdatascience.com/nlp-performance-of-different-word-embeddings-on-text-classification-de648c6262b
#https://machinelearningmastery.com/develop-word-embeddings-python-gensim/
#https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

log_flag = True

import sys
sys.path.append(".")
from TfidfEmbeddingVectorizer import TfidfEmbeddingVectorizer
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster
from sklearn import metrics
from gensim.models import KeyedVectors
from gensim.models import TfidfModel
from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords',quiet=log_flag)
nltk.download('punkt',quiet=log_flag)
import numpy as np

import time

class TCI():
    def __init__(self):
        self.filename = 'TCI/GoogleNews-vectors-negative300.bin'
        self.sample_list = []
        self.sample_list_sen = []
        self.np_centroid = np.array([])
        self.model = KeyedVectors.load_word2vec_format(self.filename,binary=True)#Word2Vec(self.filename,min_count=1)
        self.vector_size = self.model.vector_size
        self.NUM_CLUSTERS = 3
        #self.kclusterer = KMeansClusterer(self.NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
        #X = self.model[self.model.vocab]
        #self.assigned_clusters = self.kclusterer.cluster(X, assign_clusters=True)
        #print(self.assigned_clusters)
        #words = list(self.model.vocab)
        #for i, word in enumerate(words):  
            #print (word + ":" + str(self.assigned_clusters[i]))
        #self.TF_IDF = TfidfVectorizer()
        #self.TF_IDF.fit_transform(self.model.vocab)
        
    def addSample(self,sample_string):
        sample_string = sample_string.translate(str.maketrans({key: None for key in string.punctuation}))
        self.sample_list_sen.append(sample_string)
        buffer_list = word_tokenize(sample_string)#list(sample_string.split(" "))
        for i in buffer_list:
            internal_buffer = i.lower()
            if internal_buffer not in stopwords.words('english') :#and internal_buffer not in self.sample_list:
                self.sample_list.append(internal_buffer)
        return self.sample_list
        #self.sample_list.append(buffer_list)
    
    def sampleTrendMean(self):
        mean = []
        for word in self.sample_list:
            if word in self.model.vocab:
                mean.append(self.model.get_vector(word))
        if not mean:
            print("No sample detected !")
            return np.zeros(self.vector_size)
        else:
            #mean = np.array(mean).mean(axis=0)
            #mean = mean.reshape(1,300)
            #print(mean.reshape(1,300).shape)
            return mean#np.average(mean)
    
    def sampleVectorMean(self,sample_string):
        sample_string = sample_string.translate(str.maketrans({key: None for key in string.punctuation}))
        buffer_list = word_tokenize(sample_string)#list(sample_string.split(" "))
        final_list = []
        mean = []
        for i in buffer_list:
            internal_buffer = i.lower()
            if internal_buffer not in stopwords.words('english'):
                final_list.append(internal_buffer)
        for word in final_list:
            if word in self.model.vocab:
                mean.append(self.model.get_vector(word))
        if not mean:
            print("No sample detected !1")
            return np.zeros(self.vector_size) 
        else:
            mean = np.array(mean).mean(axis=0)
            mean = mean.reshape(1,300)
            return mean
        
    def sampleSenTrendMean(self):
        np_score_list = np.empty((0,300))
        for i in range(len(self.sample_list_sen)):
            #print('Current string value being added from sample list: ', self.sample_list_sen[i])
            try:
                np_score_list = np.append(np_score_list,self.sampleVectorMean(self.sample_list_sen[i]),axis=0)
            except:
                pass
        
        self.np_centroid = np.mean(np_score_list,axis=0)
        return self.np_centroid
        
    def distanceCentroid(self,test_string):
        ts_vector = self.sampleVectorMean(test_string).reshape(300,)
        
        distance = np.linalg.norm(self.np_centroid - ts_vector)
        return distance
    
    '''def kmeans(self):
        words = list(self.model.vocab)
        for i, word in enumerate(words):  
            print (word + ":" + str(self.assigned_clusters[i]))'''
    