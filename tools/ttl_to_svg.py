from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from rdflib import RDF, RDFS, BNode, Graph, Namespace, URIRef

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
S223 = Namespace("http://data.ashrae.org/standard223#")


def local(n):
    s = str(n)
    if "#" in s:
        return s.rsplit("#", 1)[-1]
    return s.rstrip("/").rsplit("/", 1)[-1]


def best_label(g: Graph, n) -> str:
    # Prefer rdfs:label, then skos:prefLabel, fallback to local name/str
    if isinstance(n, (URIRef, BNode)):
        for p in (RDFS.label, SKOS.prefLabel):
            lbl = g.value(n, p)
            if lbl:
                return str(lbl)
        return local(n)
    return str(n)


def safe_id(n) -> str:
    # Stable node id for DOT (not the displayed label)
    raw = n.n3() if hasattr(n, "n3") else str(n)
    h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"n_{h}"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', r"\"")


def type_locals(g: Graph, n) -> set[str]:
    ts = set()
    for t in g.objects(n, RDF.type):
        ts.add(local(t))
    return ts


def shape_attrs_for(g: Graph, n) -> dict[str, str]:
    """
    Shape rules:
    - s223:Property (and subclasses) -> circle
    - s223:ConnectionPoint (and subclasses) -> diamond (lozenge)
    - default -> box
    """
    types = type_locals(g, n)

    # Property (any *Property)
    if any(t.endswith("Property") for t in types) or "Property" in local(n):
        return {"shape": "circle"}

    # ConnectionPoints -> lozenge
    if any(t.endswith("ConnectionPoint") for t in types):
        return {"shape": "diamond"}

    # Default
    return {"shape": "box"}


# Keep only common modeling edges to reduce noise
KEEP_PREDS = {
    "contains",
    "hasMember",
    "hasConnectionPoint",
    "connectsAt",
    "connectsThrough",
    "connectedTo",
    "connectedFrom",
    "hasMedium",
    "mapsTo",
    "hasProperty",
    "observes",
    "actuatesProperty",
}


def graph_to_dot(g: Graph) -> str:
    nodes: set[URIRef | BNode] = set()
    edges: list[tuple[URIRef | BNode, str, URIRef | BNode]] = []

    for s, p, o in g:
        # only link resources to resources
        if not isinstance(s, (URIRef, BNode)) or not isinstance(o, (URIRef, BNode)):
            continue
        pred = local(p)
        if KEEP_PREDS and pred not in KEEP_PREDS:
            continue
        nodes.add(s)
        nodes.add(o)
        edges.append((s, pred, o))

    lines = [
        "digraph G {",
        '  graph [rankdir="LR"];',
        "  node [fontsize=10];",
        "  edge [fontsize=9];",
    ]

    # Define nodes with labels from RDF and shapes by type
    for n in sorted(nodes, key=lambda x: best_label(g, x).lower()):
        nid = safe_id(n)
        nlabel = esc(best_label(g, n))
        attrs = shape_attrs_for(g, n)
        # Build attributes string
        attr_str = ", ".join(
            [f'label="{nlabel}"'] + [f'{k}="{v}"' for k, v in attrs.items()]
        )
        lines.append(f"  {nid} [{attr_str}];")

    # Edges
    for s, pred, o in edges:
        sid = safe_id(s)
        oid = safe_id(o)
        lines.append(f'  {sid} -> {oid} [label="{esc(pred)}"];')

    lines.append("}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--in-dir", type=Path, required=True, help="Folder containing TTL files"
    )
    ap.add_argument("--out-dir", type=Path, required=True, help="Folder to write SVGs")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for ttl in sorted(args.in_dir.glob("*.ttl")):
        g = Graph()
        g.parse(ttl.as_posix(), format="turtle")
        dot = graph_to_dot(g)
        dot_path = args.out_dir / (ttl.stem + ".dot")
        svg_path = args.out_dir / (ttl.stem + ".svg")
        dot_path.write_text(dot, encoding="utf-8")

        # Render via Graphviz dot
        import subprocess

        subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)], check=True)
        print(f"[ttl->svg] {ttl.name} -> {svg_path.name}")


if __name__ == "__main__":
    main()
