# -- Sphinx configuration for si-builder docs ---------------------------------

import os
from datetime import datetime
from pathlib import Path


# Optionally sync ASHRAE 223 publication figures into doc/figures at build time
def _sync_s223_figures():
    try:
        from dotenv import load_dotenv  # optional

        load_dotenv()
    except Exception:
        pass
    try:
        repo_root = Path(__file__).resolve().parents[1]
        figures_dst = Path(__file__).parent / "figures"
        figures_dst.mkdir(parents=True, exist_ok=True)

        s223_folder = os.getenv("S223_FOLDER") or os.getenv("S223_FOLDER")
        roots = [Path(s223_folder)] if s223_folder else []
        guess = repo_root.parent / "223standard"
        roots += [guess, guess / "Standard_223"]

        patterns = ("Figure_*.svg", "Figure_*.png")
        copied = 0
        for root in roots:
            if not root or not root.exists():
                continue
            for sub in (
                "publication/figures",
                "Publication/figures",
                "figures",
                "Figures",
                ".",
            ):
                base = root / sub
                if not base.exists():
                    continue
                for pat in patterns:
                    for src in base.rglob(pat):
                        dst = figures_dst / src.name
                        try:
                            if not dst.exists():
                                import shutil

                                shutil.copy2(src, dst)
                                copied += 1
                        except Exception:
                            pass
        if copied:
            print(f"[s223] Copied {copied} figure(s) into {figures_dst}")
    except Exception:
        # Never fail the build because of figures
        pass


def setup(app):
    # Run before reading sources
    app.connect("builder-inited", lambda *_: _sync_s223_figures())


# -- Project information
project = "si-builder"
author = "ASHRAE 223P contributors"
copyright = f"{datetime.now():%Y}, {author}"
release = ""  # set to package version if desired

# -- General configuration
extensions = [
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
]

# Recognize Markdown (MyST) and reStructuredText
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Use Awesome Theme
html_theme = "sphinxawesome_theme"

# Root document drives the global ToC
root_doc = "index"
master_doc = "index"

# Furo-specific sidebars are not used with Awesome Theme
# html_sidebars = {}  # keep unset

# Optional theme options
html_theme_options = {
    "show_scrolltop": True,
    "awesome_external_links": True,
}

# Exclude folders from Sphinx source build
exclude_patterns = [
    "archive/**",
    "_build/**",
    # do NOT exclude _artifacts; we literal-include TTLs from there
]
