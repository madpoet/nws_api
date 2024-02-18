

import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import re

def weather_conditions_emoji(cc):
    if cc == None:
        return 'na'
    if bool(re.search(r'Thunder', cc)):
        return '🌩️ '
    if bool(re.search(r'Rain', cc)):
        return '🌧️ '
    if bool(re.search(r'Partly', cc)):
        return '🌤️ '
    if bool(re.search(r'Mostly', cc)):
        return '🌥️ '
    if bool(re.search(r'Cloudy|Overcast', cc)):
        return '☁️ '
    if bool(re.search(r'Rain', cc)):
        return '🌧️ '
    if bool(re.search(r'Snow', cc)):
        return '🌨️ '
    if bool(re.search(r'Fog', cc)):
        return '🌁 '
    if bool(re.search(r'Clear|Sunny', cc)):
        return '☀️ '
    
def currentobservation(station):
    try:
        current_path = 'https://api.weather.gov/stations/' + station + '/observations/latest'
        r = requests.get(current_path)
        return r
    except:
        return ('error')
    
#pass a grid class, to lookup local station name.
def lookup_station(local_grid):
    return local_grid.station

#Get local Timezone and DST status and return in seconds from UTC
def tzoffset():
    return time.timezone * -1 if (time.localtime().tm_isdst == 0) else (time.altzone * -1)

#Convert a NWS API timestamp - Assumes that the time string is UTC
""" You could add %z in place of +00:00 and make this timezone aware """
def convert_timestamp(time_string):
        return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S+00:00') + timedelta(seconds=tzoffset())
        #+ timedelta(seconds=tzoffset())

def convert_temp(temp, to='standard'):
    if to == 'standard':
        return temp * (9/5) + 32
    else:
        return (temp - 32) * 5/9

def convert_ws(wind, to='standard'):
    if to == 'standard':
        return wind / 1.609
    else:
        return wind * 1.609

def convert_distance(distance, to='standard'):
    if to == 'standard':
        return distance * 3.281
    else:
        return distance / 3.281

def convert_precip(depth, to='standard'):
    if to == 'standard':
        return depth / 25.4
    else:
        return depth * 25.4
    
def int_to_cardinal(direction):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(direction / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


class Observation:
    def __init__(self, station, units='standard'):
        self._current_observation = currentobservation(station)    
        self._units = units
        self._station = station

    
    """ def refresh(self, station, units='standard'):
        self._current_observation = currentobservation(station=station, units=units)
     """


    @property
    def observation(self):
        return self._current_observation.json()['properties']
    
    @property
    def units(self):
        return self._units
    
    @units.setter
    def units(self, units):
        self._units = units
    
    @property
    def station(self):
        return self._station
    
    @property
    def temperature(self):
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])
        temp = self._current_observation.json()['properties']['temperature']['value']
        if temp != None:
            if self._current_observation.json()['properties']['temperature']['unitCode'] == 'wmoUnit:degC' and self._units == 'standard':
                temp = convert_temp(float(temp), self._units)
            else:
                temp = float(temp)

        return [temp, ts]
    
    @property
    def feelslike(self):
        like = 0
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])
        if self._current_observation.json()['properties']['heatIndex']['value'] != None:
            like = self._current_observation.json()['properties']['heatIndex']['value']
            #like = convert_temp(float(like), self._units)
        elif self._current_observation.json()['properties']['windChill']['value'] != None:
            like = self._current_observation.json()['properties']['windChill']['value']
            #like = convert_temp(float(like), self._units)
        elif self._current_observation.json()['properties']['temperature']['value'] != None: 
            like = self._current_observation.json()['properties']['temperature']['value']
            #like = convert_temp(float(like), self._units)
        else:
            like = self._current_observation.json()['properties']['temperature']['value']
        

        if self._current_observation.json()['properties']['temperature']['unitCode'] == 'wmoUnit:degC' and self._units == 'standard':
            like = convert_temp(float(like), self._units)
        else:
            like = float(like)
        
        
        return [like, ts]
    
    @property
    def windspeed(self):
        if self._current_observation.json()['properties']['windSpeed']['value'] != None:
            ws = convert_ws(self._current_observation.json()['properties']['windSpeed']['value'], self._units)
        else:
            ws = 0.0
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])

        return [ws, ts]
    
    @property
    def wind_direction(self):

        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])
        wd = int_to_cardinal(self._current_observation.json()['properties']['windDirection']['value'])

        return [wd, ts]

    @property
    def conditions(self):
        cd = self._current_observation.json()['properties']['textDescription']
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])

        return [cd, ts]
    
    @property
    def emoji(self):
        cd = self._current_observation.json()['properties']['textDescription']
        cd = weather_conditions_emoji(cd)
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])

        return [cd, ts]
        
    
    @property
    def icon_path(self):
        return self._current_observation.json()['properties']['icon']
    
    @property
    def humidity(self):

        hy = self._current_observation.json()['properties']['relativeHumidity']['value']
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])

        return [hy, ts]
    
    @property
    def precipitation(self):

        prc = convert_precip(self._current_observation.json()['properties']['precipitationLastHour']['value'], self._units)
        ts = convert_timestamp(self._current_observation.json()['properties']['timestamp'])

        return [prc, ts]
    


    @property
    def timestamp(self):
        return convert_timestamp(self._current_observation.json()['properties']['timestamp'])