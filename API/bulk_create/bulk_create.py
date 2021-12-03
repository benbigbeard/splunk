from csv import DictReader
import requests

# create role
# curl -k -u <USER>:<PASSWORD> https://localhost:8089/services/authorization/roles -d name=test1 -d imported_roles=user

# create user
# curl -k -u <USER>:<PASSWORD> https://localhost:8089/services/authentication/users -d name=User1 -d password=changeme -d roles=admin
# 'defaultApp': row['team']

# curl to requests - https://curl.trillworks.com/

"""
user = '<USER>'
password = '<PASSWORD>'
address = 'https://localhost:8089/services/authorization/roles'
ulist = '/Users/blovley/Desktop/Customers/Babcock/hackathon/Admin/hackathon.csv'
"""
user = ''
password = ''
address = ''
ulist = ''


# open file in read mode
with open(ulist, 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
    	if not row['exclude']:
    		# create roles
    		data = {'name': row['role'], 'imported_roles': 'user'}
    		response = requests.post(address, data=data, verify=False, auth=(user, password))
	    	# create app - https://docs.splunk.com/Documentation/Splunk/6.1.3/RESTAPI/RESTapps#POST_apps.2Flocal
	    	if row['app'] == "TRUE":
	    		data = {'name': row['team'], 'label': row['team'], 'template': 'sample_app', 'visible': '1'}
	    		response = requests.post(address, data=data, verify=False, auth=(user, password))
	    	# create users - assigned to apps (https://docs.splunk.com/Documentation/Splunk/7.2.4/RESTREF/RESTaccess#authentication.2Fusers)
	    	data = {'name': row['username'], 'password': row['password'], 'roles': row['role'], 'defaultApp': row['team']}
	    	response = requests.post(address, data=data, verify=False, auth=(user, password))
