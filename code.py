# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:15:10 2021

@author: maria
"""

# Python Code to Generate a WordCloud 
  
# Importing the Libraries 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import cv2 as cv2
from PIL import Image #to load image

# Read file  
data = pd.read_csv(r"Processed_Comments.txt", encoding ="latin-1") 

#Setting the comment and stop words
comment_words = '' 
stop_words = set(STOPWORDS) 
# Iterating through the .csv data file 
for i in data.CONTENT: 
    i = str(i) 
    seperate = i.split() 
    for j in range(len(seperate)): 
       seperate[j] = seperate[j].lower() 
      
    comment_words += " ".join(seperate)+" "
# Create the Word Cloud
#img = np.array(Image.open("C:/Users/maria/Desktop/loc.png"))
final_wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='white', colormap='gist_heat', collocations=False, stopwords = STOPWORDS)
final_wordcloud.generate(str(comment_words)) 
           
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(final_wordcloud,interpolation="bilinear") 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 
