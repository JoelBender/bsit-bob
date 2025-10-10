# TopBraid Validation

This directory contains scripts to build and run a Docker image that uses
the *TopBraid SHACL API*, an open source implementation of the W3C Shapes
Constraint Language (SHACL) based on Apache Jena.

## Source
We can clone this repo or use the repo in this folder

- https://github.com/TopQuadrant/shacl

## Build
### x86
- docker build -f .docker/Dockerfile -t ghcr.io/topquadrant/shacl:1.4.3 --build-arg VERSION=1.4.3 --build-arg ARCH_BASE=eclipse-temurin:11-alpine .

### ARM
- docker build -f .docker/Dockerfile -t ghcr.io/topquadrant/shacl:1.4.3 --build-arg VERSION=1.4.3 --build-arg ARCH_BASE=amazoncorretto:11-alpine3.18-jdk .

## merge-graphs.sh

This script combines all of the 223 and QUDT Quantity Kinds and Units into a
single `223standard.ttl` file to make it easier to copy into the image and
reference from the validation script.

## validate-build.sh

After the merge step this runs docker build.

## validate-run.sh

This script runs the `validate.py` application inside the container, mapping
the current working directory as the `/data` directory.  It runs using the
current user and group identities for the output files, assuming that the
current working directory is writable.

The script is provided a TTL file:

    $ ./validate-run.sh test-001.ttl

And it will generate a "compiled" model file that includes the triples inferred
by the 223 rules, a "report" TTL file that is the SHACL validation report, and a
colorized "report" text file that's easier to read.

    $ cat test-001.report.txt 
    s223: <http://.../pd-sr-mp-pritoni#HVACZone1TemperatureSetpoint> has Aspect-Setpoint but is not referenced by any Property using hasSetpoint.
        http://.../pd-sr-mp-pritoni#HVACZone1TemperatureSetpoint


