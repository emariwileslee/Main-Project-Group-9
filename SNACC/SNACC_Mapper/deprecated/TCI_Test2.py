# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 10:28:27 2021

@author: emari
"""

import sys
import numpy as np
sys.path.append("..\TCI\.")
from Trend_Connection_Identifier import TCI
import time

start = time.time()

text1 = 'Happy Wednesday Owls!!! Today is the last day of the meet our team campaign and we are featuring Alex and his burrow! We hope you have enjoyed getting to know our 2021 Orientation Leaders 🦉✨'
text2 = '“Life’s most persistent and urgent question is, what are you doing for others?” Today is a day on, and our Orientation Leaders are up early serving our community. #MLKDayofService'
text3 = 'fau rules, go owls!'

testtext = 'london bridge is falling down in spain with the queen doing a sacred dance on the sun from jupiter'#'tiger tony eats frosted flakes on wallstreet in nyc'#'go owls'

instance = TCI(2)
model_time = time.time()

score_list = []
np_score_list = np.empty((0,300))
print("Model load time:",model_time-start,"seconds")

instance.addSample(text1)
#score_list.append(instance.sampleTrendMean())
instance.addSample(text2)
#score_list.append(instance.sampleTrendMean())
sample_list = instance.addSample(text3)
sample_list = instance.addSample(testtext)
#score_list.append(instance.sampleTrendMean())
sample_list = instance.sample_list_sen


#score_list.append(instance.sampleVectorMean(text1))
#score_list.append(instance.sampleVectorMean(text2))
#score_list.append(instance.sampleVectorMean(text3))

np_score_list = np.append(np_score_list,instance.sampleVectorMean(text1),axis=0)
np_score_list = np.append(np_score_list,instance.sampleVectorMean(text2),axis=0)
np_score_list = np.append(np_score_list,instance.sampleVectorMean(text3),axis=0)

customtext = instance.sampleVectorMean(text1)

centroid = instance.sampleTrendMean()#np.mean(score_list,axis=0)
np_centroid = np.mean(np_score_list,axis=0)
real_centroid = instance.sampleSenTrendMean()

tt_vector = instance.sampleVectorMean(testtext).reshape(300,)

print("Initial text data: ",testtext)
testDistance = np.linalg.norm(centroid - tt_vector)
print("This is the distance of your vector from the initial centroid(SENTENCE-CENTROID): ",instance.distanceCentroid(testtext))
print("This is the distance of your vector from the initial centroid(WORD-CENTROID): ",testDistance)
#distance = np.linalg.norm(centroid - score_list[2].reshape(300,))
#instance.distanceCentroid(testtext)
print("Inference time:",time.time()-model_time,"seconds")

instance.kmeans()
#example = instance.sampleVectorCompile()