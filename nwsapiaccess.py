import requests
import json

#Pass a Zone ID and retrieve current active weather alerts
def activealert(szone):
    return requests.get('https://api.weather.gov/alerts/active/zone/' + szone)

#*********************************************************************
#NOTE: This is section is made up of requests of the NWS API, specifcally
#forecast data and observations for the previous six days or so.
#This data is mostly returned as JSON data, as well as some 
#methods you can use to build http requests. See
#https://www.weather.gov/documentation/services-web-api
#for details on different types of queries 
#************************************************************************ 

#Return forecast grid from lat/long
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
        "an unaccounted for error occurred"

#Get the hourly forecast for 7 days  by passing the lat/long as a string
#currently returns as a json request
def gethourlyforecast(lat_long):
    #look up grid and reporting office
    r = getGrid(lat_long)
    if r.ok:
        spath = r.json()['properties']['forecastHourly']
        try:
            r = requests.get(spath)
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
    else:
        print('un unexpected error has happened')
        
#Get daily forecast for the next seven days
#by passing lat and long (same as gethourlyforecast)
def getforecast(lat_long):
    #look up grid and reporting office
    r = getGrid(lat_long)
    if r.ok:
        spath = r.json()['properties']['forecast']
        try:
            r = requests.get(spath)
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
    else:
        print('un unexpected error has happened')

#retrieve NOAA Forecast API observed history as pandas dataset
#NOTE: There is a limit of around six days
#if you need more, dip into the GHNCD NOAA API data
# to use pass the lat long, start date and end date 
# in YYYY-MM=DDTHH:MM:SSZ format  
def getdaily(lat_long, startdate, enddate):
    station = localstation(lat_long)
    try:
        r = requests.get('https://api.weather.gov/stations/' + station + \
        '/observations?start=' + startdate + \
            '&end=' + enddate + '&limit=500')
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

#Return the low forecast temperature and time as list
def forecastlow(sloc):
    r = gethourlyforecast(sloc)
    ctemp = forecasthigh(sloc)
    for i in r.json()['properties']['periods']:
        itemp =  float(i['temperature'])
        if itemp < ctemp:
            ts = (i['startTime'])
            ctemp = itemp

    return ([ctemp, ts])

#Return the high forecast temperature and time as list
def forecasthigh(sloc):
    r = gethourlyforecast(sloc)
    ctemp = 0.0
    for i in r.json()['properties']['periods']:
        itemp =  float(i['temperature'])
        if itemp > ctemp:
            ts = (i['startTime'])
            ctemp = itemp

    return ([ctemp, ts])

#get observation stations by lat/long
def localstations(lat_long):
    r = getGrid(lat_long)
    path = r.json()['properties']['observationStations']
    return requests.get(path)

#throw up a quick list of stations by lat/long
def liststations(lat_long):
    r = localstations(lat_long)
    sjson = r.json()
    for i in sjson['features']:
       print(i['properties']['stationIdentifier'], '=', i['properties']['name'])
        
#return the local forecast office code
def localoffice(lat_long):
    r = getGrid(lat_long)
    return r.json()['properties']['cwa']

#Return the local zone. This is a little weird
#because I am using split and I can't find a better way to do it
#so pass a lat/long and this will return the forecast zone
def localzone(lat_long):
    r = getGrid(lat_long)
    fzone = r.json()['properties']['forecastZone']
    return fzone.rsplit('/', 1)[-1] 

#get the local obeservation station (I think, I mean it is the first station returned...)
def localstation(lat_long):
    r = localstations(lat_long)
    return r.json()['features'][0]['properties']['stationIdentifier']

#Get Forecast/Radar grid for current location (x,y)
def localgrid(lat_long):
    r = getGrid(lat_long)
    return str(r.json()['properties']['gridX']) + ',' + str(r.json()['properties']['gridY'])



#NOTE: The following allow for querying based on the station 
# name, eg KLAX

#Pass a forecast station (e.g. KLAX) and
# retrieve basic information. This data may be less
# complete than the getGrid method.
def stationGrid(station):
    try:
        r = requests.get('https://api.weather.gov/stations/' + station)
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

#Pass a forecast station (e.g. KLAX) and
# retrieve the stations latitude
def stationLat(station):
    r = stationGrid(station)
    coord = r.json()['geometry']['coordinates']
    return coord[1]
#Pass a forecast station (e.g. KLAX) and
# retrieve the stations latitude
def stationLong(station):
    r = stationGrid(station)
    coord = r.json()['geometry']['coordinates']
    return coord[0]

#Pass a forecast station (e.g. KLAX) and
# retrieve the longitude and latitude as a list
def stationLatLong(station):
    r = stationGrid(station)
    #flip the values, since they are listed as Long/Lat
    tmp = [r.json()['geometry']['coordinates'][1], r.json()['geometry']['coordinates'][0]]
    return tmp

#Get the time zone for a station
def stationTZ(station):
    r = stationGrid(station)
    return r.json()['properties']['timeZone']
