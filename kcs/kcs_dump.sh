#!/bin/bash -xe

START=0
ROWS=10000
QUERY="automation"
FILE="automation.txt"
API="https://access.redhat.com/hydra/rest/search/kcs"
PARAMS="q=${QUERY}&redhat_client=portal-search&rows=${ROWS}&start=${START}"
#PARAMS="q=${QUERY}&rows=${ROWS}&start=${START}"

# API limits pagination to 10
#for i in $(seq 0 9)
#do

  curl "${API}?${PARAMS}" > kcs_results.json

  let START+=${ROWS}

#done

rm -f ${FILE}
#for f in kcs*.json
#do
  jq -r '.response.docs[].view_uri' kcs_results.json  | grep 'solutions\|articles' | sort -u > ${FILE}
#done

exit 0
