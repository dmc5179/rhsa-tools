#!/bin/bash

API_HOST="https://access.redhat.com/hydra/rest/securitydata"


# Pull the list of all CVEs one page at a time
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

exit 0

# Pull the full details of each CVE if there is an RHSA which means there's a patch or fix for the issue
mkdir cves

for cve in $(jq -r '.[] | select(.advisories | length > 0).CVE' cve.json)
do
  if [ ! -f "cves/${cve}.json" ]
  then
    curl -X GET "${API_HOST}/cve/${cve}.json" -o "cves/${cve}.json"
  fi
done

exit 0

# Check if each CVE belongs to a product that we are currently mirroring
mkdir cves/patched
for cve in cves/*.json
do
  while read -r product
  do
    if grep -q "${product}" product_list.txt
    then
      cp "${cve}" cves/patched/
      break
    fi
  done < <(jq -r '.affected_release[].product_name' "${cve}" | sort -u)
done

exit 0
