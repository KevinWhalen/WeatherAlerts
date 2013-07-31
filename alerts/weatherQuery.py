#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import json
import os.path
from datetime import datetime, date, time, timedelta, tzinfo

#from sys import maxint
#from printKeys import printKeys

# Toggle weather or not to use the developmental responses.
dev = False
dev = True


#===============================================================================
# File locations
alertFile = '/var/www/html/dev/info.json'
keyFile = '../key'
key = ""
#===============================================================================


def timestamp():
  return '[' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + ']'


print timestamp() + " Alert monitoring system started."


def alertCheck(alertId):#, loc, locQ):
  if os.path.isfile(keyFile) and os.path.getsize(keyFile) > 0:
    try:
      with open(keyFile, 'r') as f:
        key = f.read()
      key = key.strip() # remove trailing end of line character
    except IOError:
      print timestamp() + " Error using file."
      return ""
  else:
    print timestamp() + " Missing key information."
    return ""

  json_string = ""
  if key != "" and (not dev):
    try:
      response = urllib2.urlopen('http://api.wunderground.com/api/' + str(key) + '/geolookup/conditions/q/zmw:44202.1.99999.json')
#      response = urllib2.urlopen('http://api.wunderground.com/api/' + str(key) + '/alert' + locQ +  '.json')
      json_string = response.read()
      response.close()
    except:
      print timestamp() + " Error with request"
#-------------------------------------------------------------------------------
# Use API example files for development
  elif key != "" and dev:
    try:
      with open("../exampleResponses/singleAlert.json", 'r') as f:
      #with open("../exampleResponses/emptyAlert.json", 'r') as f:
        json_string = f.read()
    except:
      print timestamp() +  " Error using file."
#-------------------------------------------------------------------------------

# Function for extracting and formatting only the needed information to JSON.
# Be very careful with quotes and test any changes thoroughly.
  def formatJsonAlert(a):#, loc):
    ++alertId
      #'","location":"' + loc + \
    newAlert = '{"id":' + str(alertId) + \
      ',"type":"' + a['type'] + \
      '","date":"' + a['date'] + \
      '","expires":"' + a['expires'] + \
      '","expires_epoch":' + a['expires_epoch'] + \
      ',"description":"' + a['description'] + \
      '","message":' + json.dumps(a['message']) + \
      ',"phenomena":"' + a['phenomena'] + \
      '","significance":"' + a['significance'] + '"}'
    return newAlert

# If there is an alert
  if json_string != "":
    cleaned_json_string = json_string.replace('/','')
    r = json.loads(cleaned_json_string) #parse json into a python object
    if os.path.isfile(alertFile) and os.path.getsize(alertFile) > 0:
      try:
        with open(alertFile, 'r+') as f:
          f.seek(-2, 2) # current: 0, begining: 1, end: 2
          #print timestamp() + " Alert count: " + str(r['response']['features']['alerts'])
          for a in r['alerts']:
            newAlert = formatJsonAlert(a)
            f.write(',\n' + newAlert)
          f.write(']\n')
      except IOError as e:
        print timestamp() + " Error with information file"
    elif not os.path.isfile(alertFile) or os.path.getsize(alertFile) == 0:
      try:
        with open(alertFile, 'w+') as f:
          f.write('[')
          for a in r['alerts']:
            newAlert = formatJsonAlert(a)
            f.write(newAlert + ',\n')
          f.seek(-2, 2) # Remove trailing comma and newline character
          f.write(']\n')
      except IOError as e:
        print timestamp() + "Error with information file"


def expirationCheck():
  if os.path.isfile(alertFile) and os.path.getsize(alertFile) > 0:
    try:
      with open(alertFile, 'r+') as fin:
        json_string = fin.read()
    except IOError as e:
      print timestamp() + " Error with information file"
    if json_string != "":
      f = json.loads(json_string)
      count = len(f)
      listOffset = 0
      for alert in range(count):
        print "alert: " + str(alert)
        print "listOffset : " + str(listOffset)
        if datetime.utcfromtimestamp(f[alert - listOffset]['expires_epoch']) < datetime.utcnow():
          del f[alert - listOffset]
          listOffset += 1
          print "deleted"
      if len(f) < count and len(f) != 0:
        try:
          with open(alertFile, 'w') as fout:
            fout.write(json.dumps(f) + '\n')
        except IOError as e:
          print timestamp() + " Error with information file"
      elif len(f) == 0:
        try:
          with open(alertFile, 'w') as fout:
            fout.write("")
        except IOError as e:
          print timestamp() + " Error with information file"
        
comment = """
        print f[alert]['expires_epoch']
        print datetime.fromtimestamp(f[alert]['expires_epoch'])
        print datetime.utcfromtimestamp(f[alert]['expires_epoch'])
        print datetime.today()
        print datetime.utcnow()
        #print datetime.fromtimestamp(f[alert]['expires_epoch'], tzinfo.tzname(datetime.today()))
        print f[alert]['expires']
"""


#-------------------------------------------------------------------------------
# Main program loop

# Program flow:
# On startup load:
# if it is not empty, load the information file storage file
#   only keep logged any alerts that have not expired
#
# Once every hour and a half:
# alertCheck queries the weather API
#   for some set of cities
#     if there is an alert it calls storeAlert
#       which appends the alert to the information JSON array
#
# Every interval (5 to 20 minutes):
# expirationCheck removes expired warnings

# Should it load that file everytime?
# Doing this as an always running job or a scheduled task?
#... I'm thinking just have it infinitly loop is a background process..

# TODO:
# Finish exception output for error logging.
###Because of the developer rate limit and the current rate model planned this 
###would not be able to make requests for multiple locations without blocking. 
# Finish adding a function that handles calling alertCheck() for every location.
#     Loads the locations...

def main():
  startTime = datetime.today()
  # 1.5 hours == 90 minutes == 5400 seconds
  alertInterval = timedelta(minutes=1)#hours=1.5)
  alertTimer = startTime - alertInterval
  # 5 minutes == 300 seconds, 20 minutes == 1200 seconds
  expireInterval = timedelta(minutes=2)
  expirationTimer = startTime - expireInterval
  # Javascript safe, unique identification
  alertId = -2147483647 #-maxint

  # Verify the integrity of any exsisting data
  #load alertFile and compare 'expires' times to today()

  # Main 
  while True == True:
    if (datetime.today() - alertTimer) >= alertInterval:
      alertTimer = datetime.today()
# Eventually may add a loop to handle finding alerts for multiple locations. 
      print timestamp() + " Alert check running"# for " + location
      alertCheck(alertId)
    if (datetime.today() - expirationTimer) >= expireInterval:
      expirationTimer = datetime.today()
      print timestamp() + " Expiration check running"# for " + location
      expirationCheck()
comment = """
"""


if __name__=="__main__":
  #alertCheck(0)
  main()



## Scraps ##
  #print json.dumps(parsed_json, sort_keys=True, indent=4, separators=(',', ': '))
  #printKeys(parsed_json)
  #print "Current temperature in %s is: %s" % (location, temp_f) 
  #for l in range(len(r['alerts'])):
  #  newAlert = formatJsonAlert(r['alerts'][l])
