#!/usr/bin/env python
# coding: utf-8

# In[51]:


# Generic Libraries
from PIL import Image
from keras.preprocessing.text import Tokenizer
import os
import pandas as pd
import numpy as np
import re,string,unicodedata
import cv2
import requests
import csv
import pickle

#Tesseract Library
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#Warnings
import warnings
warnings.filterwarnings("ignore")

#Garbage Collection
import gc

#Gensim Library for Text Processing
import gensim.parsing.preprocessing as gsp
from gensim.parsing.preprocessing import remove_stopwords
from gensim import utils

#TextBlob Library (Sentiment Analysis)
from textblob import TextBlob, Word

#Plotting Libraries
import matplotlib.pyplot as plt
import seaborn as sns


# In[52]:


#Define Directory Path
#sample_images = r'C:\Users\calli\Downloads\train_images'
test_images = r'C:\Users\calli\Documents\MATLAB\archive\bow_sample'


# In[53]:


#Custom Function to Traverse the folder
def traverse(directory):
    path, dirs, files = next(os.walk(directory))
    fol_nm = os.path.split(os.path.dirname(path))[-1]
    print(f'Number of files found in "{fol_nm}" : ',len(files))


# In[54]:


#Traversing the folders
#traverse(sample_images)
traverse(test_images)


# In[55]:


ex_txt = []   #list to store the extracted text
txt4bow = [] #list to use for bag of words

#Function to Extract Text
def TxtExtract(directory):
    """
    This function will handle the core OCR processing of images.
    """
    
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = subdir + os.sep + file
            
            img_cv = cv2.imread(filepath)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            
            text = pytesseract.image_to_string(img_rgb)
            
            x = re.sub(r'\n{2, 10}', '\n', text)
            
            ifspace = text.isspace()
            if ifspace == True:
                print(file)
                print("image does not have text")
            else:   
                print(file)
                ex_txt.extend([[file, filepath, (x.rstrip("\n"))]])
                txt4bow.extend([text])
                print(x.rstrip("\n"))
                
    fol_nm = os.path.split(os.path.dirname(subdir))[-1]
    
    print(f"Text Extracted from the files in '{fol_nm}' folder & saved to list..")


# In[56]:


#Extracting Text from JPG files in Sample Image Folder
#TxtExtract(sample_images)

#Extracting Text from JPG files in Dataset Folder
TxtExtract(test_images)


# In[57]:


with open('OCR.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['FileName', 'Filepath', 'Text']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(ex_txt)


# In[62]:


#BOW

filtered_txt = []

for n in range(len(txt4bow)):
    #remove stopwords
    filtered_sentence = remove_stopwords(txt4bow[n])
    filtered_txt.extend([filtered_sentence])



# using tokenizer 
model = Tokenizer()
model.fit_on_texts(filtered_txt)

keys = model.word_index.keys()

#print keys 
print(f'keys: {list(keys)}\n')

#create bag of words representation 
rep = model.texts_to_matrix(filtered_txt, mode='count')
print(rep)


# In[63]:


with open('BOW.csv', 'w', newline='', encoding='utf-8') as f:
    header = [keys]
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rep)


# In[85]:


#Free up memory
gc.collect()


# In[ ]:




