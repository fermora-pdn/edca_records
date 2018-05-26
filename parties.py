from pprint import pprint
import json
import datetime
import os
import sys
import getopt
import codecs
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.edca
buda = client.buda

releases = db.Releases
all_parties = buda.all_parties
parties = buda.parties

all_parties.remove({})
parties.remove({})


for release in releases.find({}):
    if len(release.get('parties', [])) > 0:
        all_parties.insert(release['parties'])


for pid in all_parties.distinct('id'):
    party = all_parties.find_one({'id': pid})
    if party:
        parties.insert_one(party)