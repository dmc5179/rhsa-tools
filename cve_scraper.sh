#!/bin/bash

API_HOST="https://access.redhat.com/hydra/rest/securitydata"

page=1

while true
do
  echo "Pulling CVE Page: ${page}"

  curl -X GET "${API_HOST}/cve.json?page=${page}" -o "cve_${page}.json"

  if [[ $(jq '.' "./cve_${page}.json" | wc -l) == 1 ]]
  then
    rm -f "./cve_${page}.json"
    break
  fi

  let "page++"

done

# Combine the pages into a single page
rm -f cve.json
for f in cve_*.json; do cat $f >> cve.json; done

# Remove the page files
rm -f cve_*.json

mkdir cves

for cve in $(jq -r '.[] | select(.advisories | length > 0).CVE' cve.json)
do
  if [ ! -f "cves/${cve}.json" ]
  then
    curl -X GET "${API_HOST}/cve/${cve}.json" -o "cves/${cve}.json"
  fi
done

exit 0
