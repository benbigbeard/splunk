#!/usr/bin/python

"""
users need ot change line 39 location, line 63 url, line 64  token, unquote 94-96 for sending data
"""

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
from argparse import RawTextHelpFormatter

# command line argument config
parser = argparse.ArgumentParser(description='The following arrguments can be set to true to iniclude the corresponding data: \n\n'+'-b = botp EV charging station\n'+'-e = evtx security', formatter_class=RawTextHelpFormatter)
parser.add_argument("-b", default="false", help="botp event")
parser.add_argument("-e", default="false", help="evtx security event")
args = parser.parse_args()

# global variables
global status
global counter

#variable for filepath of the template files
filepath = "/Users/blovley/Documents/GitHub/splunk/Misc/back2thejson/templates/"

# read the json templates
# 1. botp charger
if args.b =="true":
	with open(filepath+'botp_charger.json') as f:
		json_botp_temp = json.load(f)
		y = ['test']
		for obj in json_botp_temp:
			obj['host'] = obj['host'].replace('99999999', obj['TEST'])
		json_botp_temp = json.dumps(json_botp_temp)
		print("variable json_botp_temp: "+json_botp_temp)

# 2. EVTX Security
if args.e =="true":
	with open(filepath+'evtx_security.json') as f:
		evtx_security = json.load(f)
		print("variable evtx_security")

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

	# format the time stamp variable
	d=datetime(year, month, day, hour, minute)
	time=(calendar.timegm(d.timetuple()))
	time2=time-epoch_min
	date_time = str(datetime.fromtimestamp( time2 ))

	# variable options
	oslist = ["Windows 10 Enterprise 2004"]
	OS = str(random.choice(oslist))

	statuslist = ["true", "false"]
	# weights  for changing the frequency
	status = str(random.choices(statuslist, weights=(90,10))).strip('[]\'')

"""
	# posting data to splunk
	r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
	print (r.text)
"""

# main function
def main(unused_command_line_args):
	for i in range(1):
		mainScript(i)
		# sleep for real time data
		#time.sleep(60)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
