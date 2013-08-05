#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Takes a city, area, airport, or such and returns the lookup matches. 
# Using the Weather Underground AutoComplete does not require an API key. 

### NOT FINISHED ###

from sys import argv
#import getopt
#from getopt import getopt
#import argparse
import urllib2
import json

from printKeys import printKeys

if len(argv) == 1:
  print "Usage:"
  print './findLocationCode.py LOCATION [LOCATION2 LOCATION3...]'
  print "Where LOCATION is a city, radar area, airport, or such."
  print "Multiple locations can be looked up at once; simply seperate them by a space."
else:
  jsonString = ""
  for i in range(len(argv) - 1):
    i += 1
    try:
      response = urllib2.urlopen('http://autocomplete.wunderground.com/aq?query=' + argv[i] + '&c=US')
      jsonString = response.read()
    except:
      print "Error with request"

    if jsonString != "":
      print jsonString
      r = json.loads(jsonString) #parse json into a python object
      #printKeys(r)
