# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 21:03:00 2021

@author: Maria_Marousopoulou
"""

import pandas as pd
from nltk import word_tokenize

# Read from csv
txtData = pd.read_csv('preProcessedData.csv', sep='\t', encoding='utf-8')

txtData['comment'] = txtData['comment'].apply(lambda x: word_tokenize(x))
