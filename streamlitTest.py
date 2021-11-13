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

img = Image.open("datastream.png")
st.image(img, width=None)

st.title("Place Near Me")
st.header("An Information Retrieval Platform for Restaurants")

#streamlit run TEST.py

# Read the data from the txt file and
# place it in pandas dataframe for further processing
cwd = os.getcwd() 
print(cwd)
txtData = pd.read_csv('Comments_txt.txt', sep='\t', encoding='ISO-8859-1', header=0)

# Print the head of the dataframe to ensure data was
# loaded successfully
print(txtData.head())
st.table(txtData.head())


with st.form("my_form"):
    
    st.subheader("User's Preferences")
    
    # SLider for Preferences
    stream_preference = st.select_slider(
         'Distance vs Similarity',
         options=['Minimum Distance', 'Distance', 'Balance', 'Similarity', 
                  'Maximum Similarity'],value='Balance')
    st.write('I am leaning towards: **', stream_preference +'**')
    
    #User's query
    stream_location = st.text_input('Enter Location:', 'Λαοδίκης 22, Γλυφάδα 16674')
    
    stream_radius = st.text_input('Enter the radius for searching: ', '1000')
    stream_limit = st.text_input('Enter the limit for results to display: ', '1000')
    stream_query = st.text_input('Enter Query: ', 'French Cuisine')
    
    
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

postalCode = stream_location # Λαοδίκης 22, Γλυφάδα 16674
radius = stream_radius # 1000
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

print('New Radius: ', radius)

st.write("The user's limit:",limit)
st.dataframe(itemsListTuples)



map_data = pd.DataFrame({
   'latitude': itemsListTuples[2][4],'longitude' : itemsListTuples[2][5]}, index=[0])

#df=pd.DataFrame(itemsListTuples['4', '5'])   

#df = pd.DataFrame(df, columns = ['latitude', 'longitude'])
st.map(map_data)












