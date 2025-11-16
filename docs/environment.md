# Environment configuration (.env)

si-builder can read configuration from environment variables. Use a .env file at the repository root to keep settings local and version-agnostic.

Install python-dotenv to load .env files at runtime:

```bash
$ pip install python-dotenv
```

Then to parse the file and set the environment values:

```python
from dotenv import load_dotenv
load_dotenv()  # loads .env from current working directory or parents

# now os.getenv(...) will see values from .env
```

## Example .env
```properties
# Directory in which you cloned 223Standard
S223_FOLDER="path_to\223standard\"

# SHACL validation tool home (TopBraid Shacl)
SHACL_HOME=""path_to\si-builder\topbraid-validate\shacl-1.4.2"

# Logging
BOB_LOG="WARNING"
BOB_LOG_FILENAME="path_to\si-builder\log.txt"

# Example namespace
BOB_EX="http://example/"

# Include/Exclude predicate filters (optional)
# BOB_INCLUDE=""
# BOB_EXCLUDE=""

# Behavior flags
MANDITORY_LABEL=True
INCLUDE_CNX=False
INCLUDE_INVERSE=True
CONNECTION_HAS_MEDIUM=True
SHOW_INSPECTION_WARNINGS=False
```

## Variable Reference

| Variable | Description |
| :------- | :-----------|
| S223_FOLDER | Path to the Standard_223 folder within the 223standard repo. |
| SHACL_HOME | Path to your SHACL validation distribution (e.g., TopBraid shacl-1.4.2). |
| BOB_SAMPLES | Folder containing sample inputs/models for si-builder runs. |
| BOB_LOG | Logging level for si-builder (e.g., DEBUG, INFO, WARNING). |
| BOB_LOG_FILENAME | File path for log output. |
| BOB_EX | Base IRI used in examples or when generating simple example namespaces. |
| BOB_INCLUDE / BOB_EXCLUDE | Regular expressions for filtering predicates. |
| MANDITORY_LABEL | If true, require labels on created resources. |
| INCLUDE_CNX | If true, include explicit Connection nodes during export. |
| INCLUDE_INVERSE | If true, include inverse predicates when exporting/inspecting. |
| CONNECTION_HAS_MEDIUM | If true, assert hasMedium on Connection nodes where applicable. |
| SHOW_INSPECTION_WARNINGS | If true, emit inspection warnings. |

## Windows Tips

To set a value for the current session only:
```
set S223_FOLDER=D:\0Programmes\Ashrae\223standard
```

To persist for your user:
```
setx S223_FOLDER "D:\0Programmes\Ashrae\223standard"
```

Prefer .env for project reproducibility.