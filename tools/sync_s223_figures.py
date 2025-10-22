from __future__ import annotations

import argparse
import os
import shutil
from collections.abc import Iterable
from pathlib import Path


def find_figures(src_roots: Iterable[Path]) -> list[Path]:
    figs: list[Path] = []
    patterns = ["Figure_*.svg", "Figure_*.png"]
    for root in src_roots:
        if not root or not root.exists():
            continue
        for sub in (
            "publication/figures",
            "Publication/figures",
            "figures",
            "Figures",
            ".",
        ):
            d = root / sub
            if d.is_dir():
                for pat in patterns:
                    figs.extend(d.rglob(pat))
    # de-duplicate by name+size
    uniq, seen = [], set()
    for p in figs:
        k = (p.name, p.stat().st_size)
        if k not in seen:
            uniq.append(p)
            seen.add(k)
    return uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Destination folder inside docs (e.g., doc/_static/s223_figures)",
    )
    ap.add_argument(
        "--s223-folder", type=Path, default=None, help="Path to Standard_223 folder",
    )
    ap.add_argument(
        "--s223-dir", type=Path, default=None, help="Path to 223standard repo root",
    )
    ap.add_argument(
        "--load-dotenv",
        action="store_true",
        help="Load .env to resolve S223_FOLDER / S223_FOLDER",
    )
    args = ap.parse_args()

    if args.load_dotenv:
        try:
            from dotenv import load_dotenv  # type: ignore

            load_dotenv()
        except Exception:
            pass

    repo_root = Path(__file__).resolve().parents[1]
    doc_dir = repo_root / "doc"
    dest = args.dest or (doc_dir / "_static" / "s223_figures")
    dest.mkdir(parents=True, exist_ok=True)

    s223_folder = args.s223_folder or os.getenv("S223_FOLDER")
    s223_dir = args.s223_dir or os.getenv("S223_FOLDER")

    roots = []
    if s223_folder:
        roots.append(Path(s223_folder))
    if s223_dir:
        roots.append(Path(s223_dir))
    # also check sibling clone
    guess = repo_root.parent / "223standard"
    roots += [guess, guess / "Standard_223"]

    figures = find_figures(roots)
    if not figures:
        print(
            "[s223] No publication figures found. Check S223_FOLDER/S223_FOLDER in .env.",
        )
        return

    copied = 0
    for src in figures:
        try:
            shutil.copy2(src, dest / src.name)
            copied += 1
        except Exception as e:
            print(f"[s223][WARN] Failed to copy {src}: {e}")
    print(f"[s223] Copied {copied} figure(s) to {dest}")


if __name__ == "__main__":
    main()
