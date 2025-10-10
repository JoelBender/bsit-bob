#!/bin/bash

# the script needs to be run from its directory
pushd `dirname $0`

python3 -m venv venv
venv/bin/python -m pip install rdflib html5lib

# merge all of the TTL files into one and remove the owl:imports
venv/bin/python merge-graphs.py --no-imports \
    ../../223standard/models/*.ttl \
    ../../223standard/vocab/*.ttl \
    ../../223standard/validation/*.ttl \
    ../../223standard/inference/*.shapes.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-UNITS-ALL.ttl \
    223standard.ttl

# build the image passing in the file name
docker build \
    --tag validate:latest \
    --file validate.dockerfile \
    .

popd
