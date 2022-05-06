from http import client
from json import load
import os
from traceback import print_tb
from urllib import response
from urllib.parse import urlencode

from requests import request
import requests
import googlemaps

from datetime import datetime


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

            #print(latlng)
        except:
            #print('something went wrong')
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

def get_time_analysis(url, private_key, business_name, area_or_road):

    params = {
    'api_key_private': private_key,
    'venue_name': business_name,
    'venue_address': area_or_road
    }
    response = requests.request("POST", url, params=params)
    
    res = response.json()

    return res


GOOGLE_API_KEY = open('API_KEY.txt').read()
private_key = open('private_key.txt').read()

client = GoogleMapsClients(api_key=GOOGLE_API_KEY, address_or_zip='92660')

url_time = "https://besttime.app/api/v1f/orecasts"

dest = input("Enter Name of the Place: ")
area = input("Enter Area: ")

today = datetime.today().isoweekday()

res =  get_time_analysis(url_time, private_key, dest, area)

print(res)


print('Best Destination address is: %s' % dest_address)
print('Best time to get there are: %s' % best_time)