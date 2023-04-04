import json
import requests
from datetime import datetime, timedelta
import sys
import time

def getGrid(lat_long):
    try:
        r = requests.get('https://api.weather.gov/points/' + lat_long)
        #return r
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
    except:
        print('an unaccounted for error occurred')

def tzoffset():
    return time.timezone if (time.localtime().tm_isdst == 0) else (time.altzone * -1)
    
#Make a NWS formatted timestamp
def tstr(dt):
    if type(dt) is str:
        dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')
    return datetime.strftime(dt, '%Y-%m-%dT%H:%M:%SZ')

def dtstr(dt):
    #Some quick housekeeping
	ts = dt.replace('T', ' ')
	ts = ts.replace('+00:00', '')
	ts = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
	#account for timezone
	ts = ts -  timedelta(seconds=(tzoffset()*-1))
	#return the prettified string
	return datetime.strftime(ts, '%A, %B %-d, %Y, reported at %-I:%M %p') 

def dayspast(ndays):
    past = datetime.today() - timedelta(days=ndays)
    return past.strftime('%Y-%m-%dT%H:%M:%SZ')

def localstation(location):
    #get the local gris based on lat/long
    r = getGrid(location)
    #grab the path for the stations list
    path = r.json()['properties']['observationStations']
    #grab the json list of stations
    try:
        r = requests.get(path)
        return r.json()['features'][0]['properties']['stationIdentifier']
    except:
        return('error')
loc = sys.argv[1]
thestation = localstation(loc)


def currenttemp(station):
    current_path = 'https://api.weather.gov/stations/' + \
    station + '/observations/latest'
    try: 
        r = requests.get(current_path)
        vList = [r.json()['properties']['timestamp'],r.json()['properties']['temperature']['value']]
        return vList
    except:
        return ('error')

def previoustemp(station):
    try:
        endtime = datetime.now() + timedelta(seconds=(tzoffset()*-1))
        endtime = tstr(endtime)
        path = 'https://api.weather.gov/stations/' + station + '/observations?start=' + tstr(dayspast(1)) + '&end=' + endtime + '&limit=500'
        r = requests.get(path)
        for i in r.json()['features']:
            if type(i['properties']['temperature']['value']) == float:
                return (i['properties']['timestamp'],i['properties']['temperature']['value'])
                break
    except:
        return ('error')
    
def currentobservation(station):
    try:
        current_path = 'https://api.weather.gov/stations/' + station + '/observations/latest'
        r = requests.get(current_path)
        return r
    except:
        return ('error')

def previousobservation(station):
    endtime = datetime.now() + timedelta(seconds=(tzoffset()*-1))
    endtime = tstr(endtime)
    path = 'https://api.weather.gov/stations/' + station + '/observations?start=' + tstr(dayspast(1)) + '&end=' + endtime + '&limit=500'
    try:
        r = requests.get(path)
        obspath = r.json()['features'][0]['properties']['@id']
        try:
            rp = requests.get(obspath)
            return rp
        except:
            return ('error - bad path')
    except:
        return ('error')
    

#Flag for no current
current = True
temp = currenttemp(thestation)
if temp == 'error' or not temp:
    temp = previoustemp(thestation)
    current = False
    
temperature = temp[1]
timestamp = temp[0]

if current == True:
    rc = currentobservation(thestation)
else:
    rc = previousobservation(thestation)

conditions = rc.json()['properties']['textDescription']
tempC = str(temperature)
tempF = str(temperature * (9/5) + 32)
timestamp = dtstr(timestamp)
print('It is currently',tempF,'°F/', tempC,'°C and',conditions,'on',timestamp)

    
     
    





    

    

