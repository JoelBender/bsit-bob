# Installation

The recommended way to install `Bob` is with [uv](https://docs.astral.sh/uv/):

```bash
% mkdir my-building
% cd my-building
% uv init --python 3.13
Initialized project `my-building`
% uv add bsit-bob
Using CPython 3.13.1
Creating virtual environment at: .venv
...
```

To test that it works, try creating a generic piece of equipment:

```
$ uv run python3
...
>>> from bob import Equipment, dump
>>> thing = Equipment(label="thing")
>>> dump()
```

And dump out the results:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix s223: <http://data.ashrae.org/standard223#> .

[] a s223:Connectable,
        s223:Equipment ;
    rdfs:label "thing" .
```
```{admonition} URIs may be different
:class: warning

The URIs for ASHRAE Standards 135, 223, 231 have not been
finialized and are subject to change.
```


