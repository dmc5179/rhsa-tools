#!/bin/bash

for f in cvrfs/*.json
do

  echo "Processing: $f"

  LINKS=$(jq -r '.cvrfdoc.vulnerability[].remediations.remediation.url' $f)
  if [ 0 -ne $? ]
  then
    echo "jq failed to parse: $f" >> /tmp/pull_errata.log
    continue
  fi

  for errata in $(echo $LINKS | sort -u)
  do

    RHSA=${errata##*/}
    RHSA=$(echo $RHSA | sed 's|:|-|g')

    if test -e "../access.redhat.com/errata/${RHSA}"
    then
      continue
    fi

    curl -o "../access.redhat.com/errata/${RHSA}" "${errata}" 

  done

done

exit 0
