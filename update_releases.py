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

releases = db.Releases


def main(argv):
    json_path = ''
    try:
        opts, args = getopt.getopt(argv, "hp:", ["help", "path="])
    except getopt.GetoptError:
        print ('update_releases.py -p <json_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('update_releases.py -p <json_path>')
            sys.exit()
        elif opt in ("-p", "--path"):
            json_path = arg

    if json_path == '':
        print ('debes especificar un path')
        sys.exit(2)

    print("JSON_PATH -> ", json_path)

    for filename in os.listdir(json_path):
        if filename.endswith('.json'):
            print('Processing -> ', filename)
            with open(os.path.join(json_path, filename)) as f:
                d = json.load(f)
                ocid = d['releases'][0]['ocid']
                print ('ocid -> ', ocid)
                # delete release if exists
                removed = releases.remove({"ocid": ocid}, {'justOne': False})
                if removed['n'] > 0:
                    print('replacing -> ', ocid)
                # insert release
                releases.insert_one(d['releases'][0])


if __name__ == "__main__":
    main(sys.argv[1:])

