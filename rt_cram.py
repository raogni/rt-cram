from http import client
from json import load
import os
from traceback import print_tb
from urllib import response
from urllib.parse import urlencode

from requests import request
import requests
import googlemaps

class GoogleMapsClients(object):
    lat = None
    long = None
    data_type = 'json'
    location_query = None
    api_key = None

    def __init__(self, api_key=None, address_or_zip=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception("API key is required")

        self.api_key = api_key
        self.location_query = address_or_zip
        if self.location_query != None:
            self.extract_lat_long()

    def extract_lat_long(self, location=None):
        loc_query = self.location_query
        if location != None:
            loc_query = location

        endpoint = f'https://maps.googleapis.com/maps/api/geocode/{self.data_type}'
        params = {"address":loc_query, "key": self.api_key}
        url_params = urlencode(params)
        url = f'{endpoint}?{url_params}'
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}

        latlng = {}
        
        try:
            latlng = r.json()['results'][0]['geometry']['location']

            print(latlng)
        except:
            print('something went wrong')
            pass
        lat, lng = latlng.get('lat'), latlng.get('lng')
        self.lat = lat
        self.long = lng
        
        return lat, lng

def search(self, keyword="Mexican Food", radius=5000, location=None):
    lat, lng = self.lat, self.long
    if location != None:
        lat, lng = self.extract_lat_long(location=location)
    endpoint = f'https://maps.googleapis.com/maps/api/place/nearby/search/{self.data_type}'
    params = {
        'key': self.api_key,
        'location': f'{lat},{lng}',
        'radius' : radius,
        'keyword' : keyword        
    }
    params_encoded = urlencode(params)
    places_url = f'{endpoint}?{params_encoded}'
    r = requests.get(places_url)
    if r.status_code not in range(200, 299):
        return {}
    return r.json()


GOOGLE_API_KEY = open('API_KEY.txt').read()
print(GOOGLE_API_KEY)
client = GoogleMapsClients(api_key=GOOGLE_API_KEY, address_or_zip='92660')

print(client.lat, client.long)

print(client.extract_lat_long())