###############################################
#CDO Database access via station id
#This requires a token. Visit https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted
#to get started and visit https://www.ncdc.noaa.gov/cdo-web/token
#for a token and then set module.token = noaa API key
# you can also edit this file and add your API token
#perhaps future versions will include a settings file
#to include the API taken
#once it is set, you do not need to worry about passing the header when
#making requests of the CDO databases 
###############################################

import requests
import json
token = 'get a token'

#Function to process CDO requests
def getgeneric(spath):
    r=''
    r = requests.get(spath, headers={'token':token})
    if r:
        #return something
        if r.ok == True:
            if len(r.text) == 2:
                print('empty array')
                return r
            else:
                return r
    else:
        print('unknown error')
        
#Get daily mesurements up to one year by station from the GHNCD datatset
#Note, this data is only available in one year chunks and you probably
#want to select a subset of data types, because you will reach the 
#query limit of 1000 pretty fast.
#Pass CDO Station, start and end dates in 'YYYY-MM-DD'
#format. Optionally include a list of data types (and other things too)
#by passing '&datatypeid=TMAX' etc. This will be appended
#to the end of the query.
#since 
def getCDOHistory(station, startdate, enddate, stypes):
    #Start assembling a URL to pass to get history
    spath = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=' + station
    spath = spath + '&startdate=' + startdate + '&enddate=' + enddate + '&limit=1000'
    if stypes: 
        spath = spath + '&' + stypes 
    return getgeneric(spath)

# Pass the zip code and get a JSON reply of CDO stations in the area  
def CDOStations(zip_code):
    r = getgeneric('https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=ZIP:' + str(zip_code))
    if not r:
        print('no stations found. Check zip code')
    else:
        return r

#Throw up a list of CDO stations on the screen
def listCDOStations(zip_code):
    rst = CDOStations(zip_code)
    if not rst:
        print('unknown error')
    else:
        for i in rst.json()['results']:
            print(i['id'], '=', i['name'])
                   
#Get CDO Station info
def CDOStationInfo(station):
    return getgeneric('https://www.ncei.noaa.gov/cdo-web/api/v2/stations/' + station)

#Get min date of data for a station 
def CDOStationMinDate(station):
    r = CDOStationInfo(station) 
    return r.json()['mindate']

#Get min date of date for a station
def CDOStationMaxDate(station):
    r = CDOStationInfo(station) 
    return r.json()['maxdate']
