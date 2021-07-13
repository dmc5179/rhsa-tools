#!/bin/bash

API_HOST="https://access.redhat.com/hydra/rest/securitydata"

page=1

while true
do
  echo "Pulling CVRF Page: ${page}"

  curl -X GET "${API_HOST}/cvrf.json?page=${page}" -o "cvrf_${page}.json"

  if [[ $(jq '.' "./cvrf_${page}.json" | wc -l) == 1 ]]
  then
    rm -f "./cvrf_${page}.json"
    break
  fi

  let "page++"

done

# Combine the pages into a single page
rm -f cvrf.json
for f in cvrf_*.json; do cat $f >> cvrf.json; done

# Remove the page files
rm -f cvrf_*.json

mkdir cvrfs

for cvrf in $(jq -r '.[].RHSA' cvrf.json)
do
  if [ ! -f "cvrfs/${cvrf}.json" ]
  then
    curl -X GET "${API_HOST}/cvrf/${cvrf}.json" -o "cvrfs/${cvrf}.json"
  fi
done

exit 0
