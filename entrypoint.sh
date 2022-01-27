#!/bin/bash

echo "Unpacking data files..."
tar -xf access.redhat.com.tgz -C .
mv access.redhat.com/* .

echo "Rewriting source for: $HOSTNAME"

echo "Starting application..."
python3 main.py
