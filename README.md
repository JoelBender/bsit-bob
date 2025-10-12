# SI-Builder

[![Build status](https://github.com/ChristianTremblay/bsit-bob/blob/main/.github/workflows/python-package.yml?branch=main&label=build&style=flat-square)](https://github.com/ChristianTremblay/bsit-bob)

Build ASHRAE 223P–compliant models using YAML and Python. si-builder emits RDF (Turtle) and aligns key concepts with RealEstateCore.

Install

```bash
% mkdir my-building
% cd my-building
% uv init --python 3.13
Initialized project `my-building`
% uv add bsit-bob
# or uv pip install ".[tests,validation,templates,doc]", choose what you need
Using CPython 3.13.1
Creating virtual environment at: .venv
```

Verify import
```python
# ipython
import bob  # si-builder package
```

Environment
- Install python-dotenv (recommended). si-builder automatically loads a .env at the project root if present.
- See doc/environment.md for available variables and effects.

Run tests
- Windows (PowerShell)
```powershell
cd d:\0Programmes\Ashrae\si-builder
pytest .\tests\
```
- Linux (bash)
```bash
cd /path/to/si-builder
pytest tests/
```

Build documentation (HTML)
This runs helpers, executes examples to generate TTL, renders SVG graphs, and builds Sphinx.

Prerequisites (one-time)
- Windows (PowerShell)
```powershell
python -m pip install -U sphinx myst-parser rdflib graphviz python-dotenv sphinxawesome-theme
choco install graphviz
```
- Linux (bash)
```bash
python3 -m pip install -U sphinx myst-parser rdflib graphviz python-dotenv sphinxawesome-theme
sudo apt-get update && sudo apt-get install -y graphviz  # Debian/Ubuntu
# Fedora:
sudo dnf install -y graphviz
# Arch:
sudo pacman -S graphviz
```

Build and open
- Windows (PowerShell)
```powershell
python .\tools\build_docs.py
Start-Process .\doc\_build\html\index.html
```
- Linux (bash)
```bash
python3 ./tools/build_docs.py
xdg-open ./doc/_build/html/index.html
```

Docs contents (from doc/index.md)
- Getting Started
- Environment
- Core
- Enumerations
- Basics
- Syntax Operators
- Syntax
- Connections
- Junctions and Boundaries
- Sensors and Observation
- Controllers and BACnet
- References
- Systems vs Equipment
- Equipment
- Spaces
- Properties
- External References
- Templates and Catalog
- Validation and Export
- Examples from Tests
- Operators Implementation