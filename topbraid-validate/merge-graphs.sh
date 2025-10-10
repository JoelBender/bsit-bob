#!/bin/bash

python3 merge-graphs.py --no-imports --clean \
    ../../223standard/models/*.ttl \
    ../../223standard/vocab/*.ttl \
    ../../223standard/validation/*.ttl \
    ../../223standard/inference/*.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-UNITS-ALL.ttl \
    223standard.ttl

