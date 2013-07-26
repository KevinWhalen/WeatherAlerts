#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import json
import os.path

alertFile = '../info.json'
keyFile = '../key'
key = ""
if os.path.isfile(keyFile) and os.path.getsize(keyFile) > 0:
  try:
    with open(keyFile, 'r') as f:
      key = f.read()
  except IOError:
    print "Error opening key file."
    #return 1
else:
  print "Missing key or key file."

