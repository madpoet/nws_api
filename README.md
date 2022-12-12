# National Weather Service and NOAA CDO Data 
Easy access to US National Weather Service API and  NOAA CDO databases.

## National Weather Service Forecast API Access
Currently, the National Weather Service allows access to forecast data, as well as a limited period of observed data (*about six days*). Currently this data is freely available, though those requirements may change in a future versions of the API. For more information visit [**NWS WEB API**](https://www.weather.gov/documentation/services-web-api)

### nwsapiaccess
#### Usage:
This data can be accessed via latitude and longitude passed as a string. This streamlines much of the grunt work of extracting data sources. This being the initial release, nwsaccess will be changing frequently when it becomes clear what other data needs to be extracted.

Data includes hourly, daily forecasts, weather observations, stations, active weather alerts, and assorted datapoints that can be used to make more advanced queries. 

Since this is all pretty basic on the code side, grabbing other data should be pretty straightforward.

## NOAA Climate Data Online API Access
This is a set of tools to query the CDO databases provided.Visit [**Climate Data Online API**](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted) to get started.
### cdostations  
CDO Database access via observation station id This requires a token. Visit [**CDO API Key**](https://www.ncdc.noaa.gov/cdo-web/token) to request a token and then set module.token = noaa API key or edit cdostations

#### Usage
To get started try querying (getCDOStations) by zip code to retrieve the local observation stations.

Presently all data is selected by station ID's from GSOM (Monthly Summary) and GHNCD (Daily Observations) datasets.


##### Note:
*Version: .001: this code is very basic, with limited error checking. Hopefully I can rectify that in the next update*
