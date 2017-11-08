#!/bin/bash

mongoexport -d buda -c RecordPackages --out RecordPackages.json --jsonArray
mongoexport -d buda -c Records --out contratacionesabiertas_bulk.csv --type=csv --fieldFile ../fieldFile.txt
 