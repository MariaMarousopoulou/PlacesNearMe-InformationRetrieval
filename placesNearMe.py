# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 20:55:44 2021

@author: Maria_Marousopoulou
"""

import requests
from geopy.geocoders import Nominatim

clientId = 'JUTODQMHVDELCGSSCA2QMNW3L1X0G53AXPK5QTQDHIJCUTTO'
clientSecret = 'CGBRVW5AEW4GQBW21UII25BYSTZLUHGFV3044GJZRDKEPTRW'
url = 'https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id=' + clientId + '&client_secret=' + \
      clientSecret + '&v=20211018'

postalCode = input('Enter address: ')  # Λαοδίκης 22, Γλυφάδα 16674
radius = input('Enter the radius for searching: ')  # 1000
limit = input('Enter the limit for results to display: ')  # 1000

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
