# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 10:38:28 2021

@author: Maria_Marousopoulou
"""

import pandas as pd
from autocorrect import spell
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

sidewayEmoticons = [':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
                    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
                    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
                    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
                    '<3', ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
                    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
                    ':c', ':{', '>:\\', ';(']

# Load data
txtData = pd.read_csv('dataset_ubicomp2013_tips.txt', sep='\t', encoding='ISO-8859-1')

# Save to csv before preprocess
txtData.to_csv('rawData.csv', sep=';', encoding='utf-8', index=False, header=True)

txtData.columns = ['ID', 'Comment']

# Missing values
txtData.isnull().sum()  # No missing values

txtData['Comment'] = txtData['Comment'].str.lower()  # convert to lowercase

# Remove extra whitespaces
txtData['Comment'] = txtData['Comment'].apply(lambda x: ' '.join(x.split()))

# Remove AM/PM
txtData['Comment'] = txtData['Comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  ('(?:\d{2}|\d{1})(?:AM|PM|am|pm)')]))
# Remove url
txtData['Comment'] = txtData['Comment'].str.replace(r'http\S+', '')

# Remove emojis
txtData['Comment'] = txtData['Comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  sidewayEmoticons]))
# Remove symbols
txtData['Comment'] = txtData['Comment'].str.replace(r'[^\w\s]+', '')

# All to string
txtData['Comment'] = txtData['Comment'].apply(str)

# Spelling corrections
txtData['Comment'] = [' '.join([spell(i) for i in x.split()]) for x in txtData['Comment']]

# Porter Stemmer
nltkPorterStemmer = PorterStemmer()
txtData['Comment'].apply(lambda x: [nltkPorterStemmer.stem(y) for y in x])

# NLTK Stopwords;
nltkStopwords = stopwords.words('english')
txtData['Comment'] = txtData['Comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  nltkStopwords]))
# Save to csv
txtData.to_csv('processedData.csv', sep=';', encoding='utf-8', index=False, header=True)

# Read from csv to check
# newTxtData = pd.read_csv('processedData.csv', sep=';', encoding='utf-8')
