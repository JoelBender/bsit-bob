# SI-Builder Documentation

.. Bob Documentation Master File

Bob
===

**Bob** is one of a family of Python packages for building RDF representations of
building systems, the building spaces that they serve, and the measurement and
control points used to provide a safe and comfortable environment for the building
occupants. The package family members are affectionately named after the
characters of the children's television series
`Bob the Builder <https://en.wikipedia.org/wiki/List_of_Bob_the_Builder_characters>`_.

This library uses `rdflib <https://rdflib.readthedocs.io/en/stable/>`_ and
assumes that the user is familiar with the
`Resource Description Framework <https://www.w3.org/RDF/>`_ and
`RDF Schema <https://www.w3.org/TR/rdf12-schema/>`_.

**ASHRAE 223 Semantic Data Model for Analytics and Automation Applications in Buildings**

This standard defines the RDF classes and properties for a "knowledge graph"
that can be used to automate the data mapping and configuration needed to deploy
analytical, management, and control applications for the built environment.  For
more information about the standard contact **ASHRAE** or visit
`Open223 <https://open223.info>`_.

**Bob** defines Python classes that coorespond to the RDF classes in the standard
with shortcuts for common graph construction operations.  For example a `Fan` is
a subclass of `Equipment` that has inlet and outlet connection points for `Air`.

Workflow
--------

When `Bob` applications instantiate a `Fan` or some other concept there are
RDF statments added to a in-memory graph which can then be queried and/or dumped
to a Turtle file or some other RDF serialization for import into other Semantic
Web tools::

    from bob import dump
    from bob.equipment.hvac.fan import Fan

    fan = Fan(label="F1")
    dump()

Will output a TTL file like this, along with lots of other statements::

    @prefix bob: <http://data.ashrae.org/standard223/si-builder#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix s223: <http://data.ashrae.org/standard223#> .

    _:bee9 a s223:Connectable,
          s223:Equipment,
          s223:Fan ;
        rdfs:label "F1" ;
        s223:hasConnectionPoint _:b598,
          _:bd78,
          _:b2ed ;
        bob:airInlet _:bd78 ;
        bob:airOutlet _:b2ed .

Table of Content
----------------

```{toctree}
:maxdepth: 2
:numbered:

getting-started.md
environment.md
namespaces.md
subclass.md
schema-graph.md
basic_properties.md
basic_connections.md
more-connections.md
core.md
enum.md
basics.md
syntax-operators.md
syntax.md
connections.md
junctions-and-boundaries.md
sensors-and-observation.md
controllers-and-bacnet.md
references.md
systems-vs-equipment.md
equipment.md
spaces.md
properties.md
externalreferences.md
templates-and-catalog.md
validation-and-export.md
examples-from-tests.md
operators-implementation.md
glossary.md
```

Notes
- Cross-references align with ASHRAE 223P classes (see links in each page).
