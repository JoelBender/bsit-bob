from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path):
    print(f"[examples] {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=str(cwd))


def main():
    repo = Path(__file__).resolve().parents[1]
    doc = repo / "doc"
    examples_dir = doc / "examples"
    manifest = examples_dir / "examples.json"
    artifacts = doc / "_artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    if not manifest.is_file():
        print(f"[examples] No manifest: {manifest} (skipping)")
        return

    data = json.loads(manifest.read_text(encoding="utf-8"))
    for name, spec in data.items():
        script = examples_dir / spec["script"]
        out_ttl = artifacts / spec["out_ttl"]
        out_ttl.parent.mkdir(parents=True, exist_ok=True)

        # Each script must accept an --out argument for TTL path
        run([sys.executable, str(script), "--out", str(out_ttl)], cwd=repo)

    print(f"[examples] Wrote TTLs to {artifacts}")


if __name__ == "__main__":
    main()
