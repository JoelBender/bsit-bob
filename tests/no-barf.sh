#!/bin/bash

for f in *.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python3 $f | python ../sort_turtle_file.py > ttl/$ttl
done
