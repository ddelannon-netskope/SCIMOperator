#!/usr/bin/python

import urllib3
import json
import ssl
import sys
import argparse
import requests
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="Options: delallusers / delallgroups / adduser / deluser / listalluser")
parser.add_argument("-t", "--tenant", help="Tenant name. Without '.goskope.com' suffix.")
parser.add_argument("-s", "--scimkey", help="SCIM key")
parser.add_argument("-o", "--orgid", help="Orgid token")
args = parser.parse_args()
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

url = "https://addon-" + args.tenant + ".goskope.com/SCIM/V2/" + args.orgid
payload={}
headers = { 
	'Accept': 'application/scim+json',
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + args.scimkey 
}

def delallusers (args):

	while input("It's not possible to reverse after apply this action. Do you want to delete ALL SCIM users in your tenant "+ args.tenant + ".goskope.com? [y/n]") == "y":

		response = requests.get(url + "/Users", headers=headers, data=payload, verify=False)
		json_data = json.loads(response.text)

		idallusers = []
		totalRecords = json_data['itemsPerPage']
		for i in range(0,totalRecords):
			idallusers.append (json_data['Resources'][i]['id'])

		for i in range(0,totalRecords):
			response = requests.delete(url + "/Users/" + idallusers[i], headers=headers, data=payload, verify=False)
			print ("User " + idallusers[i] + " has been deleted.")
		
		print ("")
		print ("Total of " + str(totalRecords) + " user.s deleted.")
		break


def delallgroups (args):

	while input("It's not possible to reverse after apply this action. Do you want to delete ALL the groups in your tenant "+ args.tenant + ".goskope.com? [y/n]") == "y":

		response = requests.get(url + "/Groups", headers=headers, data=payload, verify=False)
		json_data = json.loads(response.text)

		idallgroups = []
		totalRecords = json_data['itemsPerPage']
		for i in range(0,totalRecords):
			idallgroups.append (json_data['Resources'][i]['id'])

		for i in range(0,totalRecords):
			response = requests.delete(url + "/Groups/" + idallgroups[i], headers=headers, data=payload, verify=False)
			print ("Group " + idallgroups[i] + " has been deleted.")
		
		print ("")
		print ("Total of " + str(totalRecords) + " Group.s deleted.")
		break


def adduser (args):

	username = input("Enter [userName]:")
	name = input("Enter [Name]:")
	surname = input("Enter [Surname]:")
	email = input("Enter [Email]:")

	payload = json.dumps({
	  "schemas": [
	    "urn:ietf:params:scim:schemas:core:2.0:User"
	  ],
	  "userName": username,
	  "name": {
	    "familyName": surname,
	    "givenName": name
	  },
	  "active": True,
	  "emails": [
	    {
	      "value": email,
	      "primary": True
	    }
	  ]
	})

	response = requests.post(url + "/Users", headers=headers, data=payload, verify=False)	
	print ("")
	print (response)
	print ("")


def deluser (args):
	userid = input("Enter [Id]:")
	response = requests.delete(url + "/Users/" + userid, headers=headers, data=payload, verify=False)
	print ("")
	print (response)
	print ("")


def listalluser (args):
	response = requests.get(url + "/Users", headers=headers, data=payload, verify=False)
	json_data = json.loads(response.text)
	idallusers = []
	nameallusers = []
	totalRecords = json_data['itemsPerPage']
	for i in range(0,totalRecords):
		idallusers.append (json_data['Resources'][i]['id'])
		nameallusers.append (json_data['Resources'][i]['userName'])
	for i in range(0,totalRecords):
		print ("UserId: " + idallusers[i] + "  userName: " + nameallusers[i])	
	print ("")
	print ("Total of " + str(totalRecords) + " user listed.")


def noaction ():
  #defaulterrormessage
  print ("")
  print ("No action selected. Please review help for more information.")
  print ("")


if __name__ == "__main__":
  if args.action == "delallusers":
    delallusers (args)
  if args.action == "delallgroups":
    delallgroups (args)
  if args.action == "adduser":
    adduser (args)
  if args.action == "deluser":
    deluser (args)
  if args.action == "listalluser":
    listalluser (args)
  else:
    noaction ()