"""'
Module for basic NWS weather/forecast station information
data can be accesed by lat/long
or data can be retrieved by forecast station indentifier (eg; KLAX) 

Classes are pretty much read only properties of various commnaly accessed
values from the local forecast grids. Other data is available through the
json property.
TODO: change to pass lat/long as seperate values,
describe properties (document you fool)

"""

#import json
import requests


#Return forecast grid json request from lat/long
def getGrid(slocation):
    try:
        r = requests.get('https://api.weather.gov/points/' + slocation)
            #return r
        r.raise_for_status()
        return r
    except:
        return 'error'
    
#Pass a forecast station (e.g. KLAX) and
# retrieve basic information. This data may be less
# complete than the getGrid function.
def stationGrid(station):
    try:
        r = requests.get('https://api.weather.gov/stations/' + station)
        r.raise_for_status()
        return r
    except:
        return 'error'

#*********************************************************************************
#NOTE: Geocode stuff. Uses the US Census API and IP Lookup stuff
#for more information, go to 
#https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
#*********************************************************************************
def lookupcounty(latitude, longitude):
    #splitted = slocation.split(',', 0) 
    xpath = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates' 
    paras = {'x':longitude,
             'y':latitude,
             'benchmark':4,
             'vintage':4,
             'format':'json'}
    
    try:
        r = requests.get(xpath, params=paras)
        r.raise_for_status
        return [r.json()['result']['geographies']['Counties'][0]['BASENAME'], r.json()['result']['geographies']['Counties'][0]['GEOID']], r
    except:
        return 'error'
        print(r.text)

"""
Grid class. Pass a latitude/longitude (as a string, eg. 'lat,long')
this is a big class and currently takes a sec to load
currently readonly properties are availiable
"""
class Grid:
    def __init__(self, latitude, longitude):
        self._location = str(latitude) + ',' + str(longitude)
        self._grid = getGrid(self._location)
        self._county, self._geography = lookupcounty(latitude, longitude)
        #if the grid is there, get the pieces you need
        self._station_path = self._grid.json()['properties']['observationStations']
        #self._station = localstation(self._station_path)
        self._stations = requests.get(self._station_path)
        """ if self._grid.ok == True:
            self._station_path = self._grid.json()['properties']['observationStations']
            #self._zone = self._grid.json()['properties']['forecastZone'].rsplit('/',1)[1]
            #self._office = self._grid.json()['properties']['cwa']
            self._station = localstation(self._station_path)
            self._stations = requests.get(self._station_path)
            #self._timezone = self._grid.json()['properties']['timeZone']
            #self._forecastGrid = str(self._grid.json()['properties']['gridX']) + ',' + str(self._grid.json()['properties']['gridY'])
            #self._observation_path = 'https://api.weather.gov/stations/' + self._station + '/observations/latest'
            #self._forecast_path = self._grid.json()['properties']['forecast']
 """

        self._rerror = self._grid.raise_for_status
        self._rstatus = self._grid.status_code

    @property
    def grid(self):
        return self._grid.json()['properties']
    
    @property
    def geography(self):
        return self._geography.json()['result']['geographies']
    
    @property
    def county(self):
        return self._county[0]
    
    @property
    def FIPS(self):
        return self._county[1]
    
    @property
    def station_path(self):
        return self._station_path

    @property 
    def stations(self):
        '''
        A json request object containing associated stations.

        example:
        import grid as grd
        grid = grd.Grid(lat, long)
        for i in grid.stations.json()['features']:
            print(i['properties']['stationIdentifier'], ':', i['properties']['name'])

        returns:
        KSLC : Salt Lake City, Salt Lake City International Airport
        KPVU : Provo Municipal Airport
        K74V : ROOSEVELT
        ...  
        '''
        return self._stations

    @property
    def station(self):
        return self._stations.json()['features'][0]['properties']['stationIdentifier']

    @property
    def forecastGrid(self):
        return str(self._grid.json()['properties']['gridX']) + ',' + str(self._grid.json()['properties']['gridY'])

    @property
    def observation_path(self):
        return 'https://api.weather.gov/stations/' + self._station + '/observations'
    
    @property
    def forecast_path(self):
        return self._grid.json()['properties']['forecast']
    
    @property
    def zone(self):
        return self._grid.json()['properties']['forecastZone'].rsplit('/',1)[1]
    
    @property
    def office(self):
        return self._grid.json()['properties']['cwa']
    
    @property
    def timezone(self):
         return self._grid.json()['properties']['timeZone']
    
    @property
    def radar_station(self):
        return self._grid.json()['properties']['radarStation']

    @property
    def rerror(self):
         return self._rerror
    
    @property
    def rstatus(self):
         return self._rstatus

"""
get station grid info. Note this, this data may be less complete
than the local_grid data.
"""

class station_grid:
    def __init__(self, station):
        self._grid = stationGrid(station)
        """ if self._grid.ok == True:
            #self._latlong = [self._grid.json()['geometry']['coordinates'][1], self._grid.json()['geometry']['coordinates'][0]]
            self._timezone = self._grid.json()['properties']['timeZone']
            self._station_name = self._grid.json()['properties']['name']
            #self._office = self._grid.json()['properties']['cwa']
            self._zone = self._grid.json()['properties']['forecast'].rsplit('/',1)[1]
 """
        self._rerror = self._grid.raise_for_status
        self._rstatus = self._grid.status_codev


    @property
    def grid(self):
        return self._grid.json()
    
    @property
    def timezone(self):
         return self._grid.json()['properties']['timeZone']
    
    @property
    def zone(self):
        return self._grid.json()['properties']['forecast'].rsplit('/',1)[1]
    
    @property
    def latlong(self):
        return [self._grid.json()['geometry']['coordinates'][1], self._grid.json()['geometry']['coordinates'][0]]
    
    @property
    def station_desc(self):
        return self._grid.json()['properties']['name']
    
    @property
    def station(self):
        return self._grid.json()['properties']['stationIdentifier']

    @property
    def office(self):
        return self._grid.json()

    @property
    def rerror(self):
         return self._rerror
    
    @property
    def rstatus(self):
         return self._rstatus
