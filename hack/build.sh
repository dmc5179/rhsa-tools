#!/bin/bash

API_HOST="https://access.redhat.com/hydra/rest/securitydata"

TMP_DIR="/tmp/rhsa-tools"

rm -rf ${TMP_DIR}
mkdir ${TMP_DIR}

for t in cvrf cve oval
do

  # Pull the list one page at a time
  page=1

  while true
  do
    echo "Pulling ${t} Page: ${page}"

    curl -X GET "${API_HOST}/${t}.json?page=${page}" -o "${TMP_DIR}/${t}_${page}.json"

    if [[ $(jq '.' "${TMP_DIR}/${t}_${page}.json" | wc -l) == 1 ]]
    then
      rm -f "${TMP_DIR}/${t}_${page}.json"
      break
    fi

    let "page++"

  done

  # Combine the pages into a single page
  rm -f "${TMP_DIR}/${t}.json"
  for f in "${TMP_DIR}/${t}_*.json"; do cat $f >> "${TMP_DIR}/${t}.json"; done

  # Remove the page files
  rm -f ${TMP_DIR}/${t}_*.json

  mv "${TMP_DIR}/${t}.json" "./data/${t}.json"

done

# This endpoint is not paginated
curl -X GET "${API_HOST}/oval/ovalstreams.json" -o "./data/ovalstreams.json"

rm -f access.redhat.com.tgz
tar -czf access.redhat.com.tgz access.redhat.com

podman build -t quay.io/danclark/rhsa-tools:latest -f Dockerfile .

exit 0
