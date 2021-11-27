# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 22:30:06 2021

@author: John Sugar
"""

import requests
from geopy.geocoders import Nominatim
import os
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import streamlit as st
import numpy as np
from PIL import Image
import time
from scipy import spatial
from scipy.spatial import distance
import fasttext.util
from sklearn.feature_extraction.text import TfidfVectorizer
import re  
from nltk.corpus import stopwords  
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics.pairwise import cosine_similarity 



#Run using the command below
#streamlit run datastream.py

#To hide a warning streamlit message
fasttext.FastText.eprint = lambda x: None

fasttext.util.download_model('en', if_exists='ignore')  # English
ft = fasttext.load_model('cc.en.300.bin')
#ft = fasttext.load_model('yelp_review_full.bin')
df = pd.read_csv('final_comments.csv')



img = Image.open("datastream_image.png")
st.image(img, width=None)

st.title("Places Near Me")
st.header("An Information Retrieval Platform for Restaurants")

# Read the data from the txt file and
# place it in pandas dataframe for further processing
cwd = os.getcwd() 
print(cwd)

with st.form("my_form"):
    
    st.subheader("User's Preferences")
    
    # SLider for Preferences
#    stream_preference = st.select_slider(
#         'Distance vs Similarity',
#         options=['Minimum Distance', 'Distance', 'Balance', 'Similarity', 
#                  'Maximum Similarity'],value='Balance')
#    st.write('I am leaning towards: **', stream_preference +'**')
    stream_preference = st.select_slider(
         'Distance vs Similarity',
         options=['Distance','Similarity'],value='Similarity')
    st.write('I am leaning towards: **', stream_preference +'**')
    
    #User's query
    stream_location = st.text_input('Enter Location:', 'Λαοδίκης 22, Γλυφάδα 16674')
    
    stream_radius = st.text_input('Enter the radius for searching: ', '50')
    stream_limit = st.text_input('Enter the limit for results to display: ', '5')
    stream_query = st.text_input('Enter Query: ', 'Norsk salmon')
    
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.caption('Please wait for the system to evaluate your input')
        with st.spinner('Wait for it...'):
            time.sleep(1)
            st.success('Results are coming!!')  
    
    

clientId = 'JUTODQMHVDELCGSSCA2QMNW3L1X0G53AXPK5QTQDHIJCUTTO'
clientSecret = 'CGBRVW5AEW4GQBW21UII25BYSTZLUHGFV3044GJZRDKEPTRW'
url = 'https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id=' + clientId + '&client_secret=' + \
      clientSecret + '&v=20211018'

postalCode = stream_location # Λαοδίκης 22, Γλυφάδα 16674
radius = stream_radius # 300
limit = stream_limit  # 10
preference=stream_preference

geoLocator = Nominatim(user_agent='foursquare_agent')
location = geoLocator.geocode(postalCode, timeout=10)

if location is None:
    print('Address not found ... ')
else:
    print(location)

latitude = location.latitude
longitude = location.longitude
print('Latitude: ', latitude)
print('Longtitude: ', longitude)

url = url + '&ll=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(radius) + '&limit=' + str(limit)

results = requests.get(url).json()
allItems = results['response']['venues']

# List of lists of tuples
items = []
for item in allItems:
    if len(item['categories']) > 0:
        items.append([(
            item['id'],
            item['name'],
            item['categories'][0]['name'],
            item['location']['distance'],
            item['location']['lat'],
            item['location']['lng']
        )])

# Convert to list of tuples
itemsListTuples = [i for t in items for i in t]



#If slider set to similarity   
if preference=='Similarity':  
    df_name = pd.read_csv('four_square_places.csv')
#    df_name = df_name[df_name['distance'] < int(radius)]
    st.write("Filtering based on Similarity:") 
    
    #Get vector of user's input
    vectquery = ft.get_sentence_vector(stream_query) 
    
    predictions=[]
    for line in df[df.columns[1]]:
        pred_label=ft.get_sentence_vector(line)
        predictions.append(pred_label)
    
    IDs=[]
    for line in df[df.columns[0]]:
        IDs.append(line)
    
    comments=[]
    for line in df[df.columns[1]]:
        comments.append(line)
    
    #Get the vector of the comments
    dfcsv=pd.DataFrame(list(zip(IDs, predictions,comments)),columns=['IDs','Predictions','Comments']) 
    
    similarities_values=[]
    similarities_ids=[]
    similarities_comments=[]
    for line in dfcsv['Predictions']:
        cos_distance = 1 - spatial.distance.cosine(line, vectquery)
        similarities_values.append(cos_distance)
    
    for line in dfcsv['IDs']:
        similarities_ids.append(line)
    
    for line in dfcsv['Comments']:
        similarities_comments.append(line)
    
    #Get the cosine similarity of the user's input against every comment 
    df_similarities=pd.DataFrame(list(zip(similarities_ids, similarities_values,similarities_comments)),columns=['IDs','Predictions','Comments']) 
    
    #Sort dataframe from higher to lower similarity
    final_df = df_similarities.sort_values(by=['Predictions'], ascending=False)
    
    
    #Comment below to get the most similar comment
    top=''
    top2=''
    top=final_df.nlargest(1, ['Predictions'])
    top.reset_index(drop=True, inplace=True)
    
    top2=top['IDs'].to_string(index=False)
    top2=top2.strip()
    df2=df_name[df_name.ID==top2]
#    df2=df_name[(df_name.ID==top2) & (df_name.distance<int(radius))]
    df2.set_index('ID', inplace=True)
    st.write("Most similar:" , df2.head()) 
#    st.write("Comment was: " , top['Comments'].to_string(index=False))
#    top.set_index('Comments', inplace=True)
#    top.index = top.index + 1
    st.write("Comment was: " , top)
    
    st.write("Top " + limit + " Places:")
    
    #Get the top similarities. The 70 below is arbitary. It was placed to bring all
    #Top5 dataframe name could be top7,8,9. It saves top similarities
    top5=''
    top5=final_df.nlargest(70, ['Predictions'])
    top5.drop_duplicates(subset ="IDs",
                         keep='first', inplace = True)
    temp=[]    
    counter=1
    df3=[]
    #Iterate the top5 dataframe in order to print the most similar comments 
    for line in top5['IDs']:
        line=line.strip()
        temp=df_name.loc[df_name['ID'] == line]
        temp.set_index('ID', inplace=True)
#        print(temp['Name'])
        df3.append(temp)
        #Print in streamlit the restaurant that had this similarity 
        st.write(counter,temp) 
        counter=counter+1
        if counter > int(limit): 
            break
      
    #This is just to print the foursquare dataset   
#    st.write(df_name)
    
    
    ####################################################################
    #TFIDF

#
#    csvdata = pd.read_csv('final_comments_test.csv')
    csvdata1=pd.read_csv('processedData.csv', sep=';', encoding='utf-8')
#    df_name = pd.read_csv('four_square_places.csv')
    vectorizer = TfidfVectorizer()
    
    processed_tfidf = []
    for line in csvdata1['Comment']:
            # Remove all the special characters
        processed = re.sub(r'\W', ' ', str(line))
         
            # remove all single characters
        processed = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed)
         
            # Remove single characters from the start
        processed = re.sub(r'\^[a-zA-Z]\s+', ' ', processed) 
         
            # Substituting multiple spaces with single space
        processed= re.sub(r'\s+', ' ', processed, flags=re.I)
         
            # Removing prefixed 'b'
        processed = re.sub(r'^b\s+', '', processed)
         
            # Converting to Lowercase
        processed = processed.lower()
         
        processed_tfidf.append(processed)
        
    #print(processed_tfidf)
    
    df_tfidf1 = vectorizer.fit(processed_tfidf)
    
    df_tfidf2 = df_tfidf1.transform(processed_tfidf)
    
    df_tfidf2=df_tfidf2.toarray()
    
    
    
#    query = "Be careful with the napkins on your pants."
    query_vec = df_tfidf1.transform([stream_query])
    query_vec=query_vec.toarray()
    #Needs preprocessing the query with Textblob
    #print(query_vec)
    query_vec=query_vec.reshape(1, -1)
    
    similarities_values=[]
    similarities_comments=[]
    for line in df_tfidf2:
    #for line in range(df_tfidf2.shape(0)):
        line=line.reshape(1, -1)
        cos_distance = cosine_similarity(line, query_vec)
        similarities_values.append(cos_distance)
        
    for line in csvdata1['Comment']:
        similarities_comments.append(line)   
        
    df_similarities=pd.DataFrame(list(zip(similarities_values,similarities_comments)),
        columns=['Predictions','Comments']) 
    
    df_similarities.Predictions = df_similarities.Predictions.astype(float)
    
    df_similarities = df_similarities.sort_values(by=['Predictions'], ascending=False)
#    testss=''

#    testss=df_similarities.nlargest(1, ['Predictions'])
#    testss=df_similarities.head()
#    st.write(df_similarities.head())
#    out = np.empty(df_similarities.shape[0], dtype=object)
#    out[:] = df_similarities.values.tolist()
#    st.write(out)
    
#    from pandas.api.types import infer_dtype
#
#    for col in df_similarities.columns:
#        if infer_dtype(df_similarities[col]) == 'Predictions' : 
#    # ‘mixed’ is the catchall for anything that is not otherwise specialized
#            df_similarities[col] = df_similarities[col].astype('str')
    
#    st.write(str(df_similarities.head(1)))
    df_similarities.set_index('Predictions', inplace=True)
    st.write("Top " + limit + " Places via TF-IDF: ",df_similarities.head(int(limit)))
    
    
#If slider set to distance  
#This is a naive approach where we filter with the user's distance and
#print in ascenting order the most top results, without processing them    
if preference=='Distance':
    df_name = pd.read_csv('four_square_places.csv')
    st.write("Filtering based on Proximity:")
    counter2=1    
    dfpreference = df_name.sort_values(by=['distance'], ascending=False)
    smaller_distance = dfpreference.sort_values(['distance'], ascending=True)
    smaller_distance.set_index('ID', inplace=True)
    smaller_distance = smaller_distance[smaller_distance['distance'] < int(radius)]
    smaller_distance = smaller_distance[smaller_distance['Tag'] != 'Other']
    st.write('TFIDF Top ' + limit + ' Places by TFIDF')
    st.write(smaller_distance.head(int(limit)))


    
    
    
    
    