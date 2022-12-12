# National Weather Service and NOAA CDO Data 
Easy access to US National Weather Service and  NOAA CDO databases

# nwsapiaccess.py - 
## National Weather Service Forecast API Access
Currently, the National Weather Service allows access to forecast data, as well as a limited period of observed data (*about six days*). Currently this data is freely available, though those requirements may change in a future versions of the API. For more information visit [**NWS WEB API**](https://www.weather.gov/documentation/services-web-api)

## Usage:
Presently, this data can be accessed via latitude and longitude passed as a string. This streamlines much of the grunt work of extracting data sources. This being the initial release, nwsaccess.py will be changing frequently when it becomes clear what other data needs to be extracted.

## Data notes
Data includes hourly, daily forecasts, weather observations, stations, active weather alerts, and assorted datapoints that can be used to make more advanced queries. 

If a idea may occur to you for a piece of data to extract, feel free to submit and we can add it. Since this is all pretty basic on the code side, grabbing other data should be pretty straightforward

# cdostations.py

## NOAA Climate Data Online API Access
This is a set of tools to query the CDO databases provided. 
CDO Database access via station id
This requires a token. Visit https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted to get started and visit https://www.ncdc.noaa.gov/cdo-web/token for a token and then set module.token = noaa API key
