import importlib
import inspect
import pkgutil
from pathlib import Path

TARGET_DUNDERS = {
    "__matmul__",
    "__rshift__",
    "__rrshift__",
    "__lshift__",
    "__rlshift__",
    "__gt__",
    "__or__",
    "__ror__",
    "__add__",
    "__iadd__",
    "__sub__",
    "__isub__",
    "__truediv__",
    "__floordiv__",
    "__and__",
    "__rand__",
    "__xor__",
    "__rxor__",
}
REPORT = []


def iter_bob_modules():
    import bob

    pkg = bob
    for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        # Skip caches/checkpoints
        if any(s in m.name for s in (".__pycache__", ".ipynb_checkpoints")):
            continue
        yield m.name


def collect_dunders(modname):
    try:
        mod = importlib.import_module(modname)
    except Exception as e:
        REPORT.append(f"- [WARN] import failed: {modname}: {e}")
        return
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        # only classes defined in this module
        if getattr(obj, "__module__", "") != mod.__name__:
            continue
        dunders = sorted(set(dir(obj)) & TARGET_DUNDERS)
        if not dunders:
            continue
        REPORT.append(f"## {obj.__module__}.{obj.__name__}")
        for d in dunders:
            func = getattr(obj, d, None)
            sig = ""
            try:
                sig = str(inspect.signature(func))
            except Exception:
                pass
            doc = (inspect.getdoc(func) or "").splitlines()[0:2]
            doc = " ".join(doc).strip()
            REPORT.append(f"- {d}{sig}  —  {doc}")


def collect_multimethods():
    # scan functions decorated with singledispatch/dispatch-like attributes
    REPORT.append("\n# Multimethods and singledispatch")
    for modname in iter_bob_modules():
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue
        for fname, obj in inspect.getmembers(mod, inspect.isfunction):
            # crude heuristic: singledispatch adds .register and .dispatch
            if hasattr(obj, "register") and hasattr(obj, "dispatch"):
                sig = ""
                try:
                    sig = str(inspect.signature(obj))
                except Exception:
                    pass
                where = f"{modname}.{fname}{sig}"
                REPORT.append(f"- singledispatch: {where}")
        for fname, obj in inspect.getmembers(mod, inspect.isclass):
            # methods decorated by singledispatchmethod may appear as function descriptors
            for mname, meth in inspect.getmembers(obj, inspect.isfunction):
                if hasattr(meth, "register") and hasattr(meth, "dispatch"):
                    REPORT.append(
                        f"- singledispatchmethod: {modname}.{obj.__name__}.{mname}()"
                    )


def main():
    REPORT.clear()
    REPORT.append("# Operators (Implementation Map)\n")
    REPORT.append(
        "This page is generated from the codebase. It lists operator overloads (dunder methods) and multimethods used by si-builder to simplify modeling.\n"
    )
    for modname in iter_bob_modules():
        collect_dunders(modname)
    collect_multimethods()
    out = Path(__file__).resolve().parents[1] / "doc" / "operators-implementation.md"
    out.write_text("\n".join(REPORT), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
