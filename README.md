# National Weather Service and NOAA CDO Data

Easy access to US National Weather Service API and  NOAA CDO databases.

# National Weather Service Forecast API Access

Currently, the National Weather Service allows access to forecast data, as well as a limited period of observed data (*about six days*). Currently this data is freely available, though those requirements may change in a future versions of the API. For more information visit [**NWS WEB API**](https://www.weather.gov/documentation/services-web-api)

## nwsapiaccess

#### National Weather Service Forecast/Observation AP usage

This data can be accessed via latitude and longitude passed as a string. This streamlines much of the grunt work of extracting data sources. This being the initial release, nwsaccess will be changing frequently when it becomes clear what other data needs to be extracted.

Data includes hourly, daily forecasts, weather observation stations, active weather alerts, and assorted datapoints that can be used to make more advanced queries.

To use, try getting a list of forecast/observation stations. These are similar to airport codes, like KSLC which would be the Salt Lake International Airport. Start by querying for stations by latitiude,longitude.

`import nwsapiaccess as nws`

`nws.liststations('lat,long')`

This will produce a list of stations in that area. Most of the listed stations are observation stations.

*Note, lat long is passed as a single string 'lat,long' without a space.*

# NOAA Climate Data Online API Access

This is a set of tools to query the CDO databases provided.Visit [**Climate Data Online API**](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted) to get started.

## cdostations  

CDO Database access via observation station id This requires a token. Visit [**CDO API Key**](https://www.ncdc.noaa.gov/cdo-web/token) to request a token and then set module.token = noaa API key or edit cdostations

`import cdostations as cs`

`cs.token = your token here`

#### Climate Data Online module usage

Presently all data is selected by station ID's from GSOM (Monthly Summary) and GHCND (Daily Observations) datasets.

To get started try querying (CDOStations) by zip code to retrieve the local observation stations. You can pass either FIPS codes or ZIP code as FIPS:56041 or ZIP:90210

`import cdostations as cs`

`cs.token = *your token here*`

`cs.listCDOStations(location code)`

This will return a list of stations within in that zipcode at the python >>> prompt. You can also retrieve a json list of the same data

`import cdostations as cs`

`cs.token = *your token here*`

`r = cd.CDOStations(location code)`

`for i in r.json()['results']: print(i['id'], '=', i['name'])`

This is basically the same as listCDOStations
*Note that all CDO requests, the json record path always is found under 'results'*

##### Note

Version 001: *this code is very basic, with limited error checking. Hopefully I can rectify that in the next update*

Version 002: *Added error checking to getGrid method. This is the foundational request that selection of additional datapoints. Aditional methods for querying the NWS API by station name*
