# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 07:43:35 2021

@author: emari
"""
import sys
sys.path.append(".\yolo\.")
from yoloAPI import yoloAPI

class CLA():
    def __init__(self):
        self.yolo = yoloAPI()
        pass
    
    def yoloInvoke(self):
        self.yolo.loadImage('zebra.jpg')
        return self.yolo.initializeBoxes(True)
    
    def ocrInvoke(self):
        pass
    
    def w2vInvoke(self):
        pass
    
    def labelOutput(self):
        pass
    
instance = CLA()
test = instance.yoloInvoke()