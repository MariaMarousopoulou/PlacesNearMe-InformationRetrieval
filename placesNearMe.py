# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 20:55:44 2021

@author: Maria_Marousopoulou
"""

import time
import requests
from PIL import Image
import streamlit as st
from stemming.porter2 import stem
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from geopy.geocoders import Nominatim

# streamlit run placesNearMe.py

# Header image
img = Image.open("wallpaper.jpg")

# Title
st.title("Place Near Me")
st.header("An Information Retrieval Platform for Restaurants")

with st.form("my_form"):
    st.subheader("User's Preferences")
    # Slider for Preferences
    stream_preference = st.select_slider(
         'Distance vs Similarity',
         options=['Minimum Distance', 'Distance', 'Balance', 'Similarity', 
                  'Maximum Similarity'], value='Balance')
    st.write('I am leaning towards: **', stream_preference + '**')
    
    # User's input
    stream_location = st.text_input('Enter Location:', 'Λαοδίκης 22, Γλυφάδα 16674')
    stream_radius = st.text_input('Enter the radius for searching: ', '1000')
    stream_limit = st.text_input('Enter the limit for results to display: ', '1000')
    stream_query = st.text_input('Enter Query: ', 'A place tht serves  sushi')

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.caption('Please wait for the system to evaluate your input')
        with st.spinner('Wait for it...'):
            time.sleep(1)
            st.success('Done!')  

clientId = 'JUTODQMHVDELCGSSCA2QMNW3L1X0G53AXPK5QTQDHIJCUTTO'
clientSecret = 'CGBRVW5AEW4GQBW21UII25BYSTZLUHGFV3044GJZRDKEPTRW'
url = 'https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id=' + clientId + '&client_secret=' + \
      clientSecret + '&v=20211018'


# postalCode = input('Enter address: ')  # Λαοδίκης 22, Γλυφάδα 16674
# radius = input('Enter the radius for searching: ')  # 1000
# limit = input('Enter the limit for results to display: ')  # 1000
postalCode = stream_location  # Λαοδίκης 22, Γλυφάδα 16674
radius = stream_radius  # 1000
limit = stream_limit  # 1000


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

# userQuery = input('Enter query: ')  # A place tht serves  sushi
userQuery = stream_query  # A place tht serves  sushi

# To lowercase
userQuery = userQuery.lower()

# Remove extra whitespaces
userQuery = [x.strip() for x in userQuery.split()]

# Spelling corrections
spell = SpellChecker()
correctUserQuery = [' '.join([spell.correction(w) for w in userQuery])]

# Stemmer
correctUserQuery = [[stem(word) for word in query.split(" ")] for query in correctUserQuery]
correctUserQuery = [word for elem in correctUserQuery for word in elem]  # Flat list

# Remove stopwords
nltkStopWords = stopwords.words()
for word in correctUserQuery:
    if word in nltkStopWords: 
        correctUserQuery.remove(word)

st.write("The user's query :", correctUserQuery)
