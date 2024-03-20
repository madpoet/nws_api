"""'
Module for basic NWS weather/forecast station information
data can be accesed by lat/long
or retrieved by forecast station indentifier (eg; KLAX) 

Classes are pretty much read only properties of various commonly accessed
values from the local forecast grids. Other data is available through the
json property.

Data also includes basic geography data from the US Census API and geo coder

"""

#import json
import requests


#Return forecast grid json request from lat/long
def getGrid(slocation):
    """
    Get the grid from lat/long passed as a string ('lat,long')
    """
    try:
        r = requests.get('https://api.weather.gov/points/' + slocation)
            #return r
        r.raise_for_status()
        return r
    except:
        return 'error'
    

def station_grid(station):
    """Pass a forecast station (e.g. KLAX) and retrieve basic information. 
    This data is less complete than the Grid function."""
    try:
        r = requests.get('https://api.weather.gov/stations/' + station)
        r.raise_for_status()
        return r
    except:
        return 'error'


def stationLatlong(station):
    """
    Retrieve latitude and longitude as a list
    [latitude, longitude]
    """
    grd = stationGrid(station)
    return grd.latlong

#*********************************************************************************
#NOTE: Geocode stuff. Uses the US Census API and IP Lookup stuff
#for more information, go to
#https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
#*********************************************************************************

def lookupcounty(latitude, longitude):
    """
    Return the County name and FIPS code from lat/long and the request object
    [county, FIPS], repsonse object
    """ 
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


class Grid:
    """
    Grid class. Pass a latitude/longitude to retrieve local US NWS grid
    this is a big class and currently takes a sec to load and mostly readonly 
    properties are availiable
    """
    def __init__(self, latitude, longitude):
        self._location = str(latitude) + ',' + str(longitude)
        self._grid = getGrid(self._location)
        self._county, self._geography = lookupcounty(latitude, longitude)
        self._station_path = self._grid.json()['properties']['observationStations']
        self._stations = requests.get(self._station_path)

        self._rerror = self._grid.raise_for_status
        self._rstatus = self._grid.status_code
    
    @property
    def grid(self):
        """
        requested grid as a dictionary
        """
        return self._grid.json()['properties']
    
    @property
    def geography(self):
        """
        requested grid retrieves the geography for the lat/long 
        from US Census Geocode API
        """
        return self._geography.json()['result']['geographies']
    
   
    @property
    def county(self):
        """
        The county name for lat/long
        """
        return self._county[0]
    
    
    @property
    def FIPS(self):
        """
        The FIPS code for lat/long
        """
        return self._county[1]
    
    @property
    def stationPath(self):
        """
        URL for list stations associated with
        this grid
        """
        return self._station_path

    @property 
    def stations(self):
        """
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
        """
        return self._stations

    
    @property
    def station(self):
        """
        the NWS observation/forecast station for lat/long
    """
        return self._stations.json()['features'][0]['properties']['stationIdentifier']

    
    @property
    def forecastGrid(self):
        """
        this is the forecast grid itself, x,y as 3 digit assignment for queries
    """
        return str(self._grid.json()['properties']['gridX']) + ',' + str(self._grid.json()['properties']['gridY'])

    
    @property
    def observationPath(self):
        """
        url for weather observations for this grid
    """
        return 'https://api.weather.gov/stations/' + self._station + '/observations'
    
    
    @property
    def forecastPath(self):
        """
        url for weather forecast for this grid
    """
        return self._grid.json()['properties']['forecast']
    
    @property
    def zone(self):
        """
            forecast zone for this grid
        """
        return self._grid.json()['properties']['forecastZone'].rsplit('/',1)[1]
    
    @property
    def office(self):
        """
            NWS office for this grid
        """
        return self._grid.json()['properties']['cwa']
    
    @property
    def timezone(self):
         """
            UNIX time zone for this grid
        """
         return self._grid.json()['properties']['timeZone']
    
    @property
    def radarStation(self):
        """
            radar station for this grid
        """
        return self._grid.json()['properties']['radarStation']

    @property
    def rerror(self):
         return self._rerror
    
    @property
    def rstatus(self):
         return self._rstatus



class stationGrid:
    """
    get station grid info by passing the stain indentifier, e.g. KLAX. 
    Note, this data is less complete than the Grid data.
    """
    def __init__(self, station):
        self._grid = station_grid(station)
        #self._rerror = self._grid.raise_for_status
        #self._rstatus = self._grid.status_codev


    @property
    def grid(self):
        """This grid"""
        return self._grid.json()
    
    @property
    def timezone(self):
         """
            UNIX time zone for this grid
        """
         return self._grid.json()['properties']['timeZone']
    
    @property
    def zone(self):
        """
            forecast zone for this grid
        """
        return self._grid.json()['properties']['forecast'].rsplit('/',1)[1]
    
    @property
    def latlong(self):
        """
            latitude and longitude for this grid as a list [lat,long]
        """
        return [self._grid.json()['geometry']['coordinates'][1], self._grid.json()['geometry']['coordinates'][0]]
    
    @property
    def station_desc(self):
        """
            String name of station this grid
        """
        return self._grid.json()['properties']['name']
    
    @property
    def station(self):
        """Station for this grid (redundant, I know)"""
        return self._grid.json()['properties']['stationIdentifier']

    @property
    def office(self):
        """
            NWS office for this grid
        """
        return self._grid.json()

    @property
    def rerror(self):
         return self._rerror
    
    @property
    def rstatus(self):
         return self._rstatus
