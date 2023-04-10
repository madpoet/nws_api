# NWA/NOAA API Examples
*note: these files are presented as is. In most cases these files do not require the core modules provided by this project*

## activealerts.py
This is an example of making two queries, the first is to get the forecast grid by retrieving the forecast grid by the lattiude and longitiude. From that query the url for the alerts url is retrieved.

It returns any current weather alert for that area and displays it.

## cTemp2.py
This is an example of querying the National Weather Service Forecast API for the current temperature. Because a new observation forecast value can be null, the code includes a way of retrieving the last empty temp field. 

It also retrieves the complete observation record associated that timestamp. This code could bne massively streamlined, but is presented as a sort of scratch pad to explore some of the data.

THis returns a formatted string and displays it.




