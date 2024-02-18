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
    

def get_forecast(location):
    return location

def convert_timestamp(time_string):
        return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S-07:00') 
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

def getGrid(slocation):
    try:
        r = requests.get('https://api.weather.gov/points/' + slocation)
            #return r
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
        return 'error'
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
        return 'error'
    except:
        print('an unaccounted for error occurred', r.text)
        return 'error'

def gethourlyforecast(slocation):
    try:
        r = getGrid(slocation)
        spath = r.json()['properties']['forecastHourly']
        r = requests.get(spath)
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
        return r
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
        return r
    except:
        print('an unaccounted for error occurred')
        #return r

def getforecast(slocation):
    #look up grid and reporting office
    r = getGrid(slocation)
    spath = r.json()['properties']['forecast']
    try:
        r = requests.get(spath)
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
        return r
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
        return r
    except:
        print('an unaccounted for error occurred') 

class Forecast:
    def __init__(self, latitude, longitude, units='standard'):
        location = str(latitude) + ',' + str(longitude)
        self._current_forecast = gethourlyforecast(location).json()['properties']['periods'][0]
        self._units = units
        self._location = location
        self._timestamp = datetime.strptime(self._current_forecast['endTime'], '%Y-%m-%dT%H:%M:%S-07:00')

    
    """ def refresh(self, station, units='standard'):
        self._current_observation = currentobservation(station=station, units=units)
     """


    @property
    def forecast(self):
        return self._current_forecast
    
    @property
    def units(self):
        return self._units
    
    @units.setter
    def units(self, units):
        self._units = units

    @property
    def location(self):
        return self._location

    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def valid(self):
        return convert_timestamp(self._current_forecast['endTime'])
    
    @property
    def temperature(self):
        temp = self._current_forecast['temperature']
        if self._current_forecast['temperatureUnit'] == 'F' and self._units == 'metric':
            temp = convert_temp(self._current_forecast['temperature'], self._units)
        elif self._current_forecast['temperatureUnit'] == 'C' and self._units == 'standard':
            temp = convert_temp(self._current_forecast['temperature'], self._units)
        else:
            temp = self._current_forecast['temperature']
        return [float(temp), self._timestamp]

    @property
    def precipitation(self):
        return [self._current_forecast['probabilityOfPrecipitation']['value'], self._timestamp]
    
    @property
    def windspeed(self):
        return [float(re.findall('\d', self._current_forecast['windSpeed'])[0]), self._timestamp]
    
    @property 
    def wind_direction(self):
        return [self._current_forecast['windDirection'], self._timestamp]
    
    @property
    def conditions(self):
        return [self._current_forecast['shortForecast'], self._timestamp]
    
    @property
    def emoji(self):
        return [weather_conditions_emoji(self._current_forecast['shortForecast']), self._timestamp]


def parse_forecasts(sjson, period='12', forecastType='H'):
    total_len = len(sjson.json()['properties']['periods'])
    
    return sjson 


class Forecasts:
    def __init__(self, latitude, longitude, units='standard', forecastType='H'):
        location = str(latitude) + ',' + str(longitude)
        #if forecastType == 'H':
        self._hourly_forecasts = gethourlyforecast(location)
            #self._current_forecasts == parse_forecasts(self._forecasts, period, forecastType)
        #else:
        self._daily_forecasts = getforecast(location)

        if forecastType == 'H':
            self._forecasts = self._hourly_forecasts 
        else:
            self._forecasts = self._daily_forecasts
            
        #self._current_forecasts = parse_forecasts(self._forecasts, period, forecastType)
        

    @property
    def forecasts(self):
        return self._forecasts
    
    @property
    def forecasts_df(self):
        return pd.DataFrame.from_dict(self._forecasts.json()['properties']['periods'])
    
    @property
    def next12hours(self):
        for i in self._hourly_forecasts.json()['properties']['periods']:
            if i['number'] < 13:
                astring = str(i['temperature']) + '°F and ' + i['shortForecast'] + weather_conditions_emoji(i['shortForecast']) + \
                    ' with ' + str(i['probabilityOfPrecipitation']['value']) + \
                        '% Chance Precipitation, until ' + \
                        i['endTime']
                bstring = 'Winds ' + i['windDirection'] + ' at ' + i['windSpeed']
                print(astring + bstring)
        return pd.DataFrame.from_dict(self._hourly_forecasts.json()['properties']['periods']).query('number < 13')
        
    @property
    def next72hours(self):
        for i in self._daily_forecasts.json()['properties']['periods']:
            if i['number'] < 7:
                print(i['name'], ':', weather_conditions_emoji(i['detailedForecast']), i['detailedForecast'])
        return pd.DataFrame.from_dict(self._daily_forecasts.json()['properties']['periods']).query('number < 7')

    @property
    def next7days(self):
        for i in self._daily_forecasts.json()['properties']['periods']:
            print(i['name'], ':', weather_conditions_emoji(i['detailedForecast']), i['detailedForecast'])

        return pd.DataFrame.from_dict(self._daily_forecasts.json()['properties']['periods'])