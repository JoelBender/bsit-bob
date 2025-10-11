"""Generate catalog documentation pages (equipment, sensors, spaces, properties,
external references, connections) by introspecting bob.* packages.

Usage:
  python tools/gen_catalog_docs.py
  (Re-run whenever classes are added/removed.)

Algorithm:
- Walk submodules of each package (e.g., bob.equipment.*)
- Skip package __init__ modules
- Collect classes whose MRO includes the designated base class
- Exclude private/dunder names and names containing: base, abstract, generic
- Extract signature from __init__
- Extract first docstring line
- Extract s223 term via _class_iri / class_iri / CLASS_IRI attribute
- Write a markdown file under doc/

Generated files:
  doc/equipment.md
  doc/sensors.md
  doc/spaces.md
  doc/properties.md
  doc/externalreferences.md
  doc/connections.md
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

CATALOGS = [
    {
        "name": "equipment",
        "package": "bob.equipment",
        "base_path": "bob.core.Equipment",
        "outfile": "equipment.md",
        "title": "Built-in Equipment Classes",
        "desc": "Concrete s223:Equipment subclasses.",
    },
    {
        "name": "sensors",
        "package": "bob.sensor",  # directory is sensor/
        "base_path": "bob.core.Sensor",
        "outfile": "sensors.md",
        "title": "Built-in Sensor Classes",
        "desc": "Concrete s223:Sensor subclasses.",
    },
    {
        "name": "spaces",
        "package": "bob.space",  # directory is space/
        "base_path": "bob.core.PhysicalSpace",
        "outfile": "spaces.md",
        "title": "Built-in PhysicalSpace Classes",
        "desc": "Concrete s223:PhysicalSpace (and related) subclasses.",
    },
    {
        "name": "properties",
        "package": "bob.properties",  # directory is properties/
        "base_path": "bob.core.Property",
        "outfile": "properties.md",
        "title": "Built-in Property Classes",
        "desc": "Property subclass catalog (Observable, Actuatable, Quantifiable, Enumerable, etc.).",
    },
    {
        "name": "externalreferences",
        "package": "bob.externalreference",
        "base_path": "bob.core.ExternalReference",
        "outfile": "externalreferences.md",
        "title": "Built-in ExternalReference Classes",
        "desc": "External reference node subclasses (e.g., BACnet, InfluxDB).",
    },
    {
        "name": "connections",
        "package": "bob.connections",
        "base_path": "bob.core.Connection",
        "outfile": "connections.md",
        "title": "Built-in Connection Classes",
        "desc": "Concrete s223:Connection subclasses (typed by medium/domain).",
    },
]


def iter_modules(root_pkg_name: str) -> Iterable[str]:
    try:
        pkg = importlib.import_module(root_pkg_name)
    except ImportError:
        return []
    for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        yield m.name


def import_obj(path: str):
    """Path like 'bob.core.Equipment' -> (module, object or None)
    """
    mod_path, _, attr = path.rpartition(".")
    try:
        mod = importlib.import_module(mod_path)
        return mod, getattr(mod, attr, None)
    except Exception:
        return None, None


def is_valid_class(cls, base) -> bool:
    if not inspect.isclass(cls):
        return False
    name = cls.__name__
    if name.startswith("_") or (name.startswith("__") and name.endswith("__")):
        return False
    # must inherit base (excluding the base itself)
    if base not in inspect.getmro(cls)[1:]:
        return False
    # skip abstract / generic markers
    lname = name.lower()
    if any(tok in lname for tok in ("base", "abstract", "generic")):
        return False
    return True


def extract_signature(cls) -> str:
    try:
        sig = inspect.signature(cls.__init__)
        # remove self
        params = list(sig.parameters.values())
        if params and params[0].name == "self":
            sig = "(" + ", ".join(str(p) for p in params[1:]) + ")"
        else:
            sig = str(sig)
        return sig
    except Exception:
        return "(...)"


def extract_docline(cls) -> str:
    doc = inspect.getdoc(cls) or ""
    lines = [line.strip() for line in doc.splitlines() if line.strip()]
    return lines[0] if lines else ""


def extract_s223_term(cls) -> str | None:
    for attr in ("_class_iri", "class_iri", "CLASS_IRI"):
        iri = getattr(cls, attr, None)
        if iri is None:
            continue
        try:
            iri_str = str(iri)
        except Exception:
            continue
        if "#" in iri_str:
            local = iri_str.rsplit("#", 1)[-1]
        else:
            local = iri_str.rstrip("/").rsplit("/", 1)[-1]
        if local:
            return local
    return None


def generate_catalog(cat: dict, repo_root: Path):
    base_mod, base_cls = import_obj(cat["base_path"])
    if base_cls is None:
        print(f"[catalog] Skip {cat['name']}: base class not found {cat['base_path']}")
        return

    records = []
    visited_mods = set()
    for modname in sorted(set(iter_modules(cat["package"]))):
        if modname in visited_mods:
            continue
        visited_mods.add(modname)
        try:
            mod = importlib.import_module(modname)
        except Exception as e:
            records.append(("WARN", modname, f"import failed: {e}", "", "", None))
            continue
        mod_file = getattr(mod, "__file__", "") or ""
        if mod_file.endswith("__init__.py") or mod_file.endswith("__init__.pyc"):
            continue

        for cname, cls in inspect.getmembers(mod, inspect.isclass):
            if getattr(cls, "__module__", "") != mod.__name__:
                continue
            if not is_valid_class(cls, base_cls):
                continue
            sig = extract_signature(cls)
            docline = extract_docline(cls)
            s223_term = extract_s223_term(cls)
            records.append(("OK", modname, cname, sig, docline, s223_term))

    out = repo_root / "doc" / cat["outfile"]
    lines = []
    lines.append(
        f"<!-- Do not edit: generated by tools/gen_catalog_docs.py ({cat['name']}) -->",
    )
    lines.append(f"# {cat['title']}")
    lines.append("")
    lines.append(cat["desc"])
    lines.append("")
    lines.append(
        "Legend: Signature shows __init__ (minus self). s223 term is derived from _class_iri if present.",
    )
    lines.append("")
    current_mod = None
    for status, mod, cname, sig, docline, term in records:
        if status != "OK":
            lines.append(f"- [WARN] {mod}: {cname}")
            continue
        if mod != current_mod:
            lines.append(f"## {mod}")
            current_mod = mod
        lines.append(f"### {cname}")
        lines.append(f"- Signature: `{cname}{sig}`")
        if docline:
            lines.append(f"- Summary: {docline}")
        if term:
            lines.append(
                f"- s223 term: `{term}` (<https://explore.open223.info/s223/{term}>)",
            )
        else:
            lines.append("- s223 term: (not declared)")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[catalog] Wrote {out}")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    for cat in CATALOGS:
        generate_catalog(cat, repo_root)


if __name__ == "__main__":
    main()
