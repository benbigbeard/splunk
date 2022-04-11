#!/usr/bin/python

import argparse
import sys
import requests
import json
import time
import random
import calendar
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import sys
sys.path.insert(0, '/Users/blovley/Documents/GitHub/splunk/Misc/back2thejson/templates')
from botp_charger import jsonDict

json = json.load(jsonDict)

print = json

# command line argument config
parser = argparse.ArgumentParser(description='Connfig for the demo events')
parser.add_argument("-i", default="temp_charger", help="index")
parser.add_argument("-m", default="charger", help="host")
parser.add_argument("-n", default="charger_1", help="Machine Name")
parser.add_argument("-d", default="charger", help="Domain")
parser.add_argument("-f", default="demo3", help="File")
args = parser.parse_args()

# global variables
global status
global index
global host
global machinename
global domains
global file
global OS
global counter

# convert to strings  for json
index = str(args.i)
host = str(args.m)
machinename = str(args.n)
domain = str(args.d)
file = str(args.f)

# counter to add 1 for each entry
counter=0

# main function
def mainScript(iterationnumber):

	# keep for counter
	global counter

	# add one
	counter+=1

	# Splunk URL
	url='http://<URL>:8088/services/collector/event?auto_extract_timestamp=true'
	# auth header (token)
	authHeader = {'Authorization': 'Splunk <token>'}

	# data/time to start filling from
	year = 2022
	month = 4
	day = 11
	hour = 15
	minute = 12

	# how much time (60 is one min)
	epoch_min = counter*60

	d=datetime(year, month, day, hour, minute)
	time=(calendar.timegm(d.timetuple()))
	time2=time-epoch_min
	date_time = str(datetime.fromtimestamp( time2 ))

	oslist = ["Windows 10 Enterprise 2004"]
	OS = str(random.choice(oslist))

	statuslist = ["true", "false"]
	status = str(random.choices(statuslist, weights=(90,10))).strip('[]\'')

"""
	jsonDict = {
	    "host":host,
	    "index":index,
	    "sourcetype":"json_charger",
	    "source":"charger_1",
	    "event": {
	  "value": {
	    "version": 1,
	    "reading_time": date_time,
	    "chargerInformation": {
	      "identifier": date_time,
	      "type": "EV",
	      "osVersion": OS,
	      "hostName": machinename,
	      "domainName": "charger",
	      "manufacturerCultureId": 1116,
	      "manufacturerGeoId": 244,
	      "timeZoneId": "US/Pacific",
	      "version": "20.1.1.0",
	      "servicable": status,
          "domain": domain,
          "type": "interactive",
          "readingTime": date_time,
          "counter": counter
	    },

	    },
	    },
	  }

	r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
	print (r.text)
"""

def main(unused_command_line_args):
    for i in range(1):
        mainScript(i)
        #time.sleep(60)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
