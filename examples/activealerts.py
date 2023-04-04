import requests
import json
import sys

#Pass a Zone ID and retrieve current active weather alerts
def activealert(szone):
    return requests.get('https://api.weather.gov/alerts/active/zone/' + szone)


#Return forecast grid json request from lat/long
def getGrid(slocation):
    return requests.get('https://api.weather.gov/points/' + slocation)

#Return the local zone. This is a little weird
#because I am using split and I can't find a better way to do it
#so pass a lat/long and this will return the forecast zone
def localzone(slocation):
    r = getGrid(slocation)
    fzone = r.json()['properties']['forecastZone']
    return fzone.rsplit('/', 1)[-1]


#show the current alerts
j = 0
ra = activealert(localzone(sys.argv[1]))
#print(len(ra.json()['features']))
if len(ra.json()['features']) == 0:
    print('no current alerts found')
else:
    for i in ra.json()['features']:
        print('Issued: ', ra.json()['features'][j]['properties']['sent'], ' starting @', ra.json()['features'][j]['properties']['onset'])
        print('Areas affected:', ra.json()['features'][j]['properties']['areaDesc'])
        print('Storm Severity:', ra.json()['features'][j]['properties']['severity'], \
              ', Certainty:', ra.json()['features'][j]['properties']['certainty'], ', Urgency:', \
                  ra.json()['features'][j]['properties']['urgency'])
        print('***************************************************')
        print(ra.json()['features'][j]['properties']['event'])
        print(ra.json()['features'][j]['properties']['description'])
        print(ra.json()['features'][j]['properties']['instruction']) 
        print('Expires: ', ra.json()['features'][j]['properties']['expires'])
        j = j + 1
        


