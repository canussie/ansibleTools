#!/usr/bin/python
#
# Author: Ben Lewis
# Date: 29/11/2017
# version 2.0
#
# import requred python modules
#
import httplib, json, csv, re, string, sys, datetime
from base64 import b64encode

#
# function to get json dump of hostgroups 
#
def gethostgroups():
  # satellite URL
  url =  ""
  # credentials for API
  creds = b64encode(b"***:*****").decode("ascii")
  # build a basic auth header
  headers = { 'Authorization': 'Basic %s' % creds }
  # create connection
  conn = httplib.HTTPSConnection(url)
  # combine file handler with headers and api path
  conn.request("GET", "/api/v2/hostgroups", headers=headers)
  # send request, get response
  r1 = conn.getresponse()
  #print r1.status
  # if status NOT 200 exit with error
  if ( r1.status != 200 ):
    print "Error.."
    print "HTTP error code: %d" % r1.status
    print r1.reason
    return False
  #print r1.read()
  # else get response and conver to json
  else:
    #print "dumping inventory to json"
    hostsjson = json.loads(r1.read())
    # return json to caller
    return hostsjson
#
# function to get hosts assigned to passed in hostgroup
# id.
#
def gethosts(id):
  # convert int to str
  id = str(id)
  # satellite URL
  url =  ""
  # credentials for API
  creds = b64encode(b"***:****").decode("ascii")
  # build a basic auth header
  headers = { 'Authorization': 'Basic %s' % creds }
  # create connection
  conn = httplib.HTTPSConnection(url)
  # combine file handler with headers and api path
  url = "/api/v2/hostgroups/" + id + "/hosts"
  #print url
  conn.request("GET", "/api/v2/hostgroups/" + id + "/hosts", headers=headers)
  # send request, get response
  r1 = conn.getresponse()
  
  #print r1.status
  # if status NOT 200 exit with error
  if ( r1.status != 200 ):
    print "Error.."
    print "HTTP error code: %d" % r1.status
    print r1.reason
    return False
  #print r1.read()
  # else get response and conver to json
  else:
    #print "dumping inventory to json"
    hostsjson = json.loads(r1.read())
    # return json to caller
    return hostsjson

  
#
# get host group json dump
#
hgs = gethostgroups()
#
# build dict
#
d = {}
#
# loop through json results
#
for i in hgs['results']:
  # for each hostgroup, get id
  id = i['id']
  # get hostgroup name
  envname = i['name']
  # if id or hostgroup name empty, skip to next hostgroup
  if id is None or envname is None:
     continue 
  # get hosts for hostgroup
  hosts=gethosts(id)
  # print hosts
  # loop through returned hosts 
  # temp list for hosts
  templist = []
  for i in hosts['results']:
    # append hostname to temp list
    templist.append(i['name'])
    # add each host to list/array
  # check if hostgroup exists in dict
  if envname in d:
     # append hosts list to dict
     d[envname].extend(templist)
  else:
     # add host list to dict
     d[envname] = templist

# dump dictionary key/value in json
print json.dumps(d, sort_keys=True, indent=4)
