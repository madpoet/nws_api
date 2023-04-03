###############################################
#CDO Database access via station id
#This requires a token. 
#Visit https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted
#to get started and visit https://www.ncdc.noaa.gov/cdo-web/token
#for a token and then set module.token = noaa API key
#you can also edit this file and add your API token
#perhaps future versions will include a settings file
#to include the API taken once it is set, you do not need to worry about 
#passing the header when making requests of the CDO databases 
###############################################

import requests
import json
token = 'get a token'

#Function to process CDO requests
#for more information on the CDO specifications visit:
#https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted
#Return a json request from NOAA CDO database
def getgeneric(spath):
    #print(spath)
    try:
        r = requests.get(spath, headers={'token':token})
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print('HTTP CONNECION ERROR', r.text)
        print(e)
    except requests.exceptions.RequestException as e:
        print('REQUEST EXCEPTION:', r.text)
        print(e)
    except:
        print('AN UNKNOWN ERROR OCCURED: ', r.text)
        
# Get CDO data by passing location codes FIPS or ZIP codes (FIPS:56 or ZIP:90210)
# pass a start date and end date as yyyy-mm-dd format
# Optionally append additional query parameters,
# for example 'datatypeid=TMAX&units=metric'
# Optionally pass the dataset you want to query, by default this is GHCND
# The three datasets are generally GHCND (DAILY), GSOM (monthly), & GSOY (yearly)
# TODO: currently the GHCND only allows for lrss than one year of
# data to be retrieved and then a limit 1000 records.
# The GSOM and GSOY sets only allow for less than ten years.
# Future versions should include error checking for date constraints
def getCDOLocationHistory(location, startdate, enddate, stypes='', dataset='GHCND'):
    #Start assembling a URL to pass to get history
    spath = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=' + \
        dataset + '&locationid=' + location
    spath = spath + '&startdate=' + startdate + \
        '&enddate=' + enddate + '&limit=1000'
    if stypes:
        spath = spath + '&' + stypes
    print(spath)
    return getgeneric(spath)

# Get CDO data by passing a station id
# pass a start date and end date as yyyy-mm-dd forma
# Optionally append additional query parameters,
# for example 'datatypeid=TMAX&units=metric'
# Optionally pass the dataset you want to query, by default this is the GHCND
# The three datasets are generally GHCND (DAILY), GSOM(monthly)), & GSOY (yearly)
# TODO: currently the GHCND only allows for lrss than one year of data to be
# retrieved and then a limit 1000 records. The GSOM and GSOY sets only allow
# for less than ten yearas.
# Future versions should include error checking for date constraints
def getCDOStationHistory(station, startdate, enddate, stypes='', dataset='GHCND'):
    #Start assembling a URL to pass to get history
    spath = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=' + \
        dataset + '&stationid=' + station
    spath = spath + '&startdate=' + startdate + \
        '&enddate=' + enddate + '&limit=1000'
    if stypes:
        spath = spath + '&' + stypes
    #print(spath)
    return getgeneric(spath)

# Pass the location code ('ZIP:90210' or 'FIPS:56042', etc.)
# and get a JSON reply of CDO stations in the area
def CDOStations(loc_code):
    r = getgeneric('https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=' + loc_code)
    if not r:
        print('no stations found. Check location code')
    else:
        return r

# Display a list of stations
# Pass the location code ('ZIP:90210' or 'FIPS:56042', etc.)
# and get a JSON reply of CDO stations in the area
def listCDOStations(loc_code):
    rst = CDOStations(loc_code)
    if not rst:
        print('unknown error')
    else:
        for i in rst.json()['results']:
            print(i['id'], '=', i['name'])

#Get CDO Station info
def CDOStationInfo(station):
    return getgeneric('https://www.ncei.noaa.gov/cdo-web/api/v2/stations/' + station)

#Get min date of available station data
def CDOStationMinDate(station):
    r = CDOStationInfo(station)
    return r.json()['mindate']

#Get max date of available  station data
def CDOStationMaxDate(station):
    r = CDOStationInfo(station)
    return r.json()['maxdate']

#Return the available datasets for a station
def CDOStationData(station):
    return getgeneric('https://www.ncei.noaa.gov/cdo-web/api/v2/datasets?stationid=' + station)

#Return the station name
def CDOStationName(station):
    r = CDOStationInfo(station)
    return r.json()['name']
