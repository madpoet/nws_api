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
#Get the hourly forecast for 7 days  by passing the lat/long as a string
#currently returns as a json request
def gethourlyforecast(lat_long):
    #look up grid and reporting office
    r = getGrid(lat_long)
    if r.ok:
        tjson = r.json()
        spath = r.json()['properties']['forecastHourly']
        return requests.get(spath)
    else:
        print('nothing happened ', r.text) 

#Return forecast grid json request from lat/long
#error checking here 
def getGrid(slocation):
    try:
        r = requests.get('https://api.weather.gov/points/' + slocation)
        #return r
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
    
    return r

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

#retrieve NOAA Forecast API observed history as pandas dataset
#NOTE: There is a limit of around six days
#if you need more, dip into the GHNCD NOAA API data
# to use pass the lat long, start date and end date 
# in YYYY-MM=DDTHH:MM:SSZ format  
def getdaily(lat_long, startdate, enddate):
    station = localstation(lat_long)
    r = requests.get('https://api.weather.gov/stations/' + station + \
        '/observations?start=' + startdate + \
            '&end=' + enddate + '&limit=500')
    if r.ok == True:
       return r
    else:
        print("error conecting: " + r.text)
