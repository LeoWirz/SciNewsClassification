#!/usr/bin/env python

import requests
import json

BASE_URL = 'http://epfl.elasticsearch.spinn3r.com'
LOG_DIR = 'log'
DATA_DIR = 'spinner_data/'
NR_PAGES = 5

HEADERS = {
  'X-vendor': 'epfl',
  'X-vendor-auth': 'J1Hr4Qc2a9UrU9tHweEO1KFDypA'
}

####
# Define the query you want to run.

QUERY="""
{
    "size": 2,
    "query": {
        "query_string" : {
            "query" : "main:Obama"
        }
    }
}
"""


###
# generic function to just write data to disk
def handle_data(page, response):

    file_name="%04d.json" % page

    print("Writing JSON data to: %s" % file_name)

    f=open( DATA_DIR + file_name, "w" );
    f.write( response.content.decode('utf-8') )
    f.close()

###
# Perform the first request.  The URL needs to be slightly different because
# we have to specify the index name here.


print("Fetching from %s" % BASE_URL)
print("Running query: ")
print(QUERY)

url = '{0}/{1}'.format(BASE_URL, 'content*/_search?scroll=5m&pretty=true')

response = requests.post( url, headers=HEADERS, data=QUERY )

####
# now that we have the first result we have to parse in the scroll ID. The first
# page is LITERALLY just the scroll ID.

print(response.content)
data=json.loads(response.content.decode('utf-8'))

scroll_id = data["_scroll_id"]

handle_data(0,response)

print("Query took: %sms" % data["took"])
print("Total hits: %s" % data["hits"]["total"])

for page in range( 1, NR_PAGES):

    response = requests.post( BASE_URL, headers=HEADERS, data=scroll_id )

    handle_data(page,response)
    scroll_id = response.json()