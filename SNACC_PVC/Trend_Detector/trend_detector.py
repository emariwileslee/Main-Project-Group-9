# -*- coding: utf-8 -*-
"""
Created on Mon May 17 04:03:56 2021

@author: emari
"""

import tensorflow as tf
import keras as ks
from keras import Sequential
from keras import Dense
from keras import Dropout
import numpy as np
import matplotlib as plt

class trend_detector():
    def __init__(self):
        self.model = None
        pass
    
    def initializeModel(self):
        self.model = Sequential()
        self.model.add(Dense(input_dim=4,units=3,activation = 'relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=3,activation='relu'))
        self.model.add(Dense(units=2,activation='softmax'))
        
        return self.model