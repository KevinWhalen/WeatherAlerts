#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import json
import os.path
from datetime import datetime, date, time

#from sys import maxint
#from printKeys import printKeys

# Toggle weather or not to use the developmental responses.
dev = False
dev = True


#-------------------------------------------------------------------------------
# File locations
alertFile = '/var/www/html/dev/info.json'
keyFile = '../key'
key = ""
#-------------------------------------------------------------------------------


def timestamp():
  return '[' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + ']'


print timestamp() + " Alert monitoring system started."


def alertCheck(alertId):
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

# Function for extracting and formatting only the needed information to JSON
  def formatJsonAlert(a):
    ++alertId
    newAlert = '{"id":' + str(alertId) + \
      ',"type":"' + a['type'] + \
      '","date":"' + a['date'] + \
      '","expires":"' + a['expires'] + \
      '","description":"' + a['description'] + \
      '","message":"' + a['message'] + \
      '","phenomena":"' + a['phenomena'] + \
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


  #print json.dumps(parsed_json, sort_keys=True, indent=4, separators=(',', ': '))
  #printKeys(parsed_json)
  #print "Current temperature in %s is: %s" % (location, temp_f) 
  #for l in range(len(r['alerts'])):
  #  newAlert = formatJsonAlert(r['alerts'][l])


#-------------------------------------------------------------------------------
# Main program loop

# Program flow:
# On startup load:
# if the it is not empty, load the information file storage file
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

comment = """
def main():
  startTime = datetime.today()
  # 1.5 hours == 90 minutes == 5400 seconds
  alertInterval = 5400
  alertTimer = startTime + alertInterval
  # 5 minutes == 300 seconds, 20 minutes == 1200 seconds
  expireInterval = 300
  expirationTimer = startTime + expireInterval
  # Javascript safe, unique identification
  alertId = -2147483647 #-maxint

  # Verify the integrity of any exsisting data
  #load alertFile and compare 'expires' times to today()

  # Main 
  while True == True:
    if (datetime.today() - alertTimer) >= alertInterval:
      alertTimer = datetime.today()
      alertCheck(alertId)
    if (datetime.today() - alertTimer) >= expireInterval:
      expirationTimer = datetime.today()
      expirationCheck()
"""


if __name__=="__main__":
  alertCheck(0)
  #main()
