#!/bin/bash

mongoexport -d buda -c contratacionesabiertas --out contratacionesabiertas_bulk.json --jsonArray
mongoexport -d buda -c Records --out contratacionesabiertas_bulk.csv --type=csv --fieldFile fieldFile.txt
 