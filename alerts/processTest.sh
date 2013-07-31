#!/usr/bin/bash
# Testing main loop functionality.
# A similar command might be used for running and logging the Weather 
# Underground API requests in production. 

nohup ./weatherQuery.py >> alertProcessTest.log 2>&1 &
