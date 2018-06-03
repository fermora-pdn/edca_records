from string import Template
import subprocess 
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
db = client.buda

contratacionesabiertas = db.contratacionesabiertas

ca_count = db.contratacionesabiertas.count()

chunk_size = 25000

package=1
for i in range(0, ca_count, chunk_size):
	c1 = Template("mongoexport -d buda -c contratacionesabiertas --out contratacionesabiertas_bulk_paquete${package}.json --jsonArray --skip $skip --limit $limit")
	c2 = Template("mongoexport -d buda -c Records --out contratacionesabiertas_bulk_paquete${package}.csv --type=csv --fieldFile fieldFile.txt --skip $skip --limit $limit")
	command1 = c1.substitute(package=str(package), skip=str(i), limit=str(chunk_size))
	print (command1)
	subprocess.call(command1, shell=True)
	command2 = c2.substitute(package=str(package), skip=str(i), limit=str(chunk_size))
	print(command2)
	subprocess.call(command2, shell=True)
	package +=1 
