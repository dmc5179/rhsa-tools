#!/bin/bash -e

STATE="dne.txt"

START=$(tail -n 1 ${STATE})

for i in $(seq ${START} 5999999)
do

  echo "Checking solutions article: ${i}"

  if test -e "../access.redhat.com/solutions/${i}" || grep -q "${i}" "${STATE}"
  then
    continue
  fi

  echo "Processing solutions article: ${i}"

  node fetch_solutions.js "${i}" > "../access.redhat.com/solutions/${i}"

  # If the article doesn't exist or returns empty, remove it
  if ! test -s "../access.redhat.com/solutions/${i}"  || grep -q 'The page you are looking for is not here' "../access.redhat.com/solutions/${i}"
  then
    if ! grep -q "${i}" "${STATE}"
    then
      echo "${i}" >> "${STATE}"
    fi
    rm -fv "../access.redhat.com/solutions/${i}"
  fi

done
