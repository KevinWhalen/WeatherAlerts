WeatherAlerts
=============

##Basic alert system for server weather.

###Utilizes Weather Underground's developer API.

If my math is correct, or at least close enough to it, then using the 500 free
developer requests per month can allow a system to check for alerts every hour 
and a half. That is enough to have some what helpful, but not fully reliable, 
alert notifications. 

Combining an alert banner, whose data could be up to an hour and a half old, 
with a weather map, and links to Weather Underground's server weather watch, 
should make the system reliable enough to be useful.

Information is polled for and stored every hour and a half by a python script 
on the back end. When a visitor of the website comes, javascript is used to 
check the alert information file via a jQuery library AJAX request. 

Using a flat file to store the alerts is a simpler installation than using a 
database and more portable than using websockets. This systems normal operating 
conditions will store a tiny amount of information for a short period of time. 

Checking the alert file is on a timer to avoid having to coordinate updates 
with the backend system. 

---

####Use:

The main files of this project can be copied to a webserver directory for a 
demonstration of use. 

> alertBanner.css  
> demo.html  
> info.json  
> weatherAlerts.js  

Write access will be needed for info.json. 

The alerts directory should be placed elsewhere and executed as an always 
running job. So on linux something like: 

nohup ~/processes/weatherQuery.py >> ~/logs/weatherAlerts.log 2>&1 &

The script weatherQuery.py contains the variables and controls that need to be 
configured in order to interact with the Weather Underground API and this alert 
system's files. 

(The retrieval script could be also run as a scheduled job (ie. with cron) 
based on preferred accuracy and API subscription. Just set it call the alert and 
expiration check functions instead of the main function.) 

---

Weather Underground 
http://www.wunderground.com/

Licsense Terms 
http://www.wunderground.com/weather/api/d/terms.html

Logo Usage Guide 
http://www.wunderground.com/weather/api/d/docs?d=resources/logo-usage-guide

