# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 10:38:28 2021

@author: Maria_Marousopoulou
"""

import pandas as pd
from autocorrect import spell
from nltk import word_tokenize
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
txtData = pd.read_csv('dataset_ubicomp2013_tips.txt', sep='\t', encoding='ISO-8859-1', header=None)
txtData.columns = ['storeId', 'comment']

# Save to csv before preprocess
txtData.to_csv('rawData.csv', sep='\t', encoding='utf-8', index=False, header=True)

# Missing values
txtData.isnull().sum()  # No missing values

txtData['comment'] = txtData['comment'].str.lower()  # convert to lowercase

# Remove extra whitespaces
txtData['comment'] = txtData['comment'].apply(lambda x: ' '.join(x.split()))

# Remove AM/PM
txtData['comment'] = txtData['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  ('(?:\d{2}|\d{1})(?:AM|PM|am|pm)')]))
# Remove url
txtData['comment'] = txtData['comment'].str.replace(r'http\S+', '')

# Remove emojis
txtData['comment'] = txtData['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  sidewayEmoticons]))
# Remove symbols
txtData['comment'] = txtData['comment'].str.replace(r'[^\w\s]+', '')

# All to string
txtData['comment'] = txtData['comment'].apply(str)

# Spelling corrections
txtData['comment'] = [' '.join([spell(i) for i in x.split()]) for x in txtData['comment']]

# Porter Stemmer
nltkPorterStemmer = PorterStemmer()
txtData['comment'].apply(lambda x: [nltkPorterStemmer.stem(y) for y in x])

# NLTK Stopwords;
nltkStopwords = stopwords.words('english')
txtData['comment'] = txtData['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  nltkStopwords]))

# Tokenization
txtData['comment'] = txtData['comment'].apply(lambda x: word_tokenize(x))

# Remove duplicates
# txtData.drop_duplicates()

# Save to csv
txtData.to_csv('processedData.csv', sep='\t', encoding='utf-8', index=False, header=True)

# Read from csv to check
newTxtData = pd.read_csv('processedData.csv', sep='\t', encoding='utf-8')
