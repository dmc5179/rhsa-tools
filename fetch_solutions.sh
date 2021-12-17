#!/bin/bash -e

for i in $(seq 5000000 5298651)
do
  echo "Processing solutions article: ${i}"

  node fetch_cve.js "${i}" > "./access.redhat.com/solutions/${i}"

  # If the article doesn't exist or returns empty, remove it
  if ! test -s "./access.redhat.com/solutions/${i}"  || grep -q 'The page you are looking for is not here' "./access.redhat.com/solutions/${i}"
  then
    rm -fv "./access.redhat.com/solutions/${i}"
  fi

done
