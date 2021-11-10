# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 10:38:28 2021

@author: Maria_Marousopoulou
"""

import pandas as pd
from autocorrect import spell
from nltk import word_tokenize


sidewayEmoticons = [':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
                    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
                    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
                    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
                    '<3', ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
                    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
                    ':c', ':{', '>:\\', ';(']

punctuationSymbols = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

# Strip unwanted characters/markup  (e.g. HTML tags, punctuation, numbers, etc.).
# Break into tokens (keywords) on whitespace.
# Stem tokens to “root” words -> computational  comput
# Remove common stopwords (e.g. a, the, it, etc.).

# Load data
txtData = pd.read_csv('dataset_ubicomp2013_tips.txt', sep='\t', encoding='ISO-8859-1', header=None)
txtData.columns = ['storeId', 'comment']

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
txtData['comment'] = txtData['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                  punctuationSymbols]))

# All to string
txtData['comment'] = txtData['comment'].apply(str)

# Spelling corrections
txtData['comment'] = [' '.join([spell(i) for i in x.split()]) for x in txtData['comment']]

# Tokenization
txtData['comment'] = txtData['comment'].apply(lambda x: word_tokenize(x))


# Save to csv
txtData.to_csv('processedData.csv', sep='\t', encoding='utf-8', index=False, header=True)

# Read from csv
newTxtData = pd.read_csv('processedData.csv', sep='\t', encoding='utf-8')


# # NLTK Stopwords
# txtDataNltk = txtData.copy()
# nltkStopwords = stopwords.words('english')
# txtDataNltk['comment'] = txtDataNltk['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
#                                                                           nltkStopwords]))

# txtDataNltkNoSymbols = txtDataNltk.copy()  # Remove symbols
# txtDataNltkNoSymbols['comment'] = txtDataNltkNoSymbols['comment'].apply(
#     lambda x: ' '.join([word for word in x.split()
#                         if word not in sidewayEmoticons]))
# txtDataNltkNoSymbols['comment'] = txtDataNltkNoSymbols['comment'].apply(
#     lambda x: ' '.join([word for word in x.split()
#                         if word not in punctuationSymbols]))
