WeatherAlerts
=============

##Basic alert system for server weather.

###Utilizes Weather Underground's developer API.

If my math is correct, or at least close enought to it, then using the 500 free
developer requests per month can allow a system to check for alerts every hour 
and a half. That is enough to have some what helpful, but not fully reliable, 
alert notifications. 

Combining an alert banner, whos data could be up to an hour and a half old, 
with a weather map, and links to Weather Underground's server weather watch, 
should make the system reliable enough to be useful.

Information is polled for and stored every hour and a half by a python script 
on the back end. When a visitor of the website comes, javascript is used to 
check the alert information file via a jQuery library AJAX request. 

By using a flat file to store the alerts, transfer waste can be reduced by 
leveraging the fact that most browsers check for changes to requested resources 
before downloading them. A database request could send the same information to 
everypage the user visits. 

Checking the alert file is on a five minute timer to avoid having to cordinate 
updates with the backend system. 

---

Weather Underground
http://www.wunderground.com/
Licsense Terms
http://www.wunderground.com/weather/api/d/terms.html
Logo Usage Guide
http://www.wunderground.com/weather/api/d/docs?d=resources/logo-usage-guide

