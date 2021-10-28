# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:40:28 2021

@author: Maria_Marousopoulou
"""

import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction import text

sidewayEmoticons = [':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
                    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
                    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
                    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
                    '<3', ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
                    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
                    ':c', ':{', '>:\\', ';(']

# Load data
txtData = pd.read_csv('dataset_ubicomp2013_tips.txt', sep='\t', encoding='ISO-8859-1', header=None)
txtData.columns = ['storeId', 'userId', 'comment']

# Preprocess data
txtData = txtData.drop('userId', 1)  # drop user
txtData['comment'] = txtData['comment'].str.lower()  # convert to lowercase

# NLTK Stopwords
txtDataNltk = txtData.copy()
nltkStopwords = stopwords.words('english')
txtDataNltk['comment'] = txtDataNltk['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in
                                                                          nltkStopwords]))
txtDataNltkNoEmoticons = txtDataNltk.copy()
txtDataNltkNoEmoticons['comment'] = txtDataNltkNoEmoticons['comment'].apply(
    lambda x: ' '.join([word for word in x.split()
                        if word not in sidewayEmoticons]))

# SKLearn Stopwords
txtDataSklearn = txtData.copy()
sklearnStopwords = text.ENGLISH_STOP_WORDS
txtDataSklearn['comment'] = txtDataSklearn['comment'].apply(
    lambda x: ' '.join([word for word in x.split()
                        if word not in sklearnStopwords]))
txtDataSklearnNoEmoticons = txtDataSklearn.copy()
txtDataSklearnNoEmoticons['comment'] = txtDataSklearnNoEmoticons['comment'].apply(
    lambda x: ' '.join([word for word in x.split()
                        if word not in sidewayEmoticons]))
