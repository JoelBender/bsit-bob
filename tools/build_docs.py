from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path, warn_only: bool = False, label: str = "") -> None:
    tag = f"[build-docs]{('[' + label + ']') if label else ''}"
    print(f"{tag} {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, cwd=str(cwd))
    except subprocess.CalledProcessError as e:
        if warn_only:
            print(f"{tag} WARN: {e}")
        else:
            raise


def main():
    repo = Path(__file__).resolve().parents[1]
    doc = repo / "doc"

    # Load .env (optional)
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv()
    except Exception:
        pass

    # Generate docs and catalogs already configured earlier...
    run(
        [sys.executable, str(repo / "tools" / "gen_glossary_from_rdf.py")],
        cwd=repo,
        label="glossary",
    )
    run(
        [sys.executable, str(repo / "tools" / "gen_equipment_docs.py")],
        cwd=repo,
        label="equipment",
    )
    op = repo / "tools" / "gen_operator_docs.py"
    if op.is_file():
        run(
            [sys.executable, str(op)],
            cwd=repo,
            label="operators",
            warn_only=True,
        )
    run(
        [sys.executable, str(repo / "tools" / "gen_catalog_docs.py")],
        cwd=repo,
        label="catalogs",
        warn_only=True,
    )

    # 1) Run curated examples to produce TTLs under doc/_artifacts
    run(
        [sys.executable, str(repo / "tools" / "run_examples.py")],
        cwd=repo,
        label="examples",
        warn_only=True,
    )

    # 2) Convert TTLs to SVGs into _static/artifacts
    out_svgs = doc / "_static" / "artifacts"
    out_svgs.mkdir(parents=True, exist_ok=True)
    run(
        [
            sys.executable,
            str(repo / "tools" / "ttl_to_svg.py"),
            "--in-dir",
            str(doc / "_artifacts"),
            "--out-dir",
            str(out_svgs),
        ],
        cwd=repo,
        label="render",
        warn_only=True,
    )

    # 3) Sync s223 publication figures if configured
    run(
        [
            sys.executable,
            str(repo / "tools" / "sync_s223_figures.py"),
            "--load-dotenv",
            "--dest",
            str(doc / "_static" / "s223_figures"),
        ],
        cwd=repo,
        label="figures",
        warn_only=True,
    )

    # 4) Build Sphinx
    out = doc / "_build" / "html"
    out.mkdir(parents=True, exist_ok=True)
    run(
        ["sphinx-build", "-b", "html", str(doc), str(out)],
        cwd=repo,
        label="sphinx",
    )

    print(f"[build-docs] Done. Open: {out / 'index.html'}")


if __name__ == "__main__":
    main()
