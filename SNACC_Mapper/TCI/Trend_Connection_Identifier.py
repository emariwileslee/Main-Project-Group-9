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
        buffer_list = word_tokenize(sample_string)#list(sample_string.split(" "))
        for i in buffer_list:
            internal_buffer = i.lower()
            if internal_buffer not in stopwords.words('english') and internal_buffer not in self.sample_list:
                self.sample_list.append(i)
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
            mean = np.array(mean).mean(axis=0)
            return np.average(mean)
    
    def sampleVectorMean(self,sample_string):
        sample_string = sample_string.translate(str.maketrans({key: None for key in string.punctuation}))
        buffer_list = word_tokenize(sample_string)#list(sample_string.split(" "))
        final_list = []
        mean = []
        for i in buffer_list:
            internal_buffer = i.lower()
            if internal_buffer not in stopwords.words('english') and internal_buffer not in self.sample_list:
                final_list.append(i)
        for word in final_list:
            if word in self.model.vocab:
                mean.append(self.model.get_vector(word))
        if not mean:
            print("No sample detected !")
            return np.zeros(self.vector_size) 
        else:
            return mean
    
    def test(self,sample_string):
        mean = []
        for word in self.sample_list:
            if word in self.model.vocab:
                mean.append(self.model.get_vector(word))
        if not mean:
            print("No sample detected !")
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean
    
    '''def kmeans(self):
        words = list(self.model.vocab)
        for i, word in enumerate(words):  
            print (word + ":" + str(self.assigned_clusters[i]))'''
    