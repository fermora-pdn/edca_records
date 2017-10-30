#!/bin/bash

json_dir=$1
echo "Looking for JSON files -> " $json_dir

for f in $json_dir*
do
    echo 'Parsing -> ' $f
    jq -r ".releases[] " $f |  mongoimport -d edca -c Releases --type=json
done