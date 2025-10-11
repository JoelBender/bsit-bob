import importlib
import inspect
import pkgutil
import typing as t

import bob

from .core import UNIT, Substance
from .enum import Constituent, Medium, Particulate

class_cache: dict[str, type] = {}
module_cache: dict[str, list[str]] = {}
enum_cache: dict[str, type] = {}
XREF_CACHE = {
    "UNIT": UNIT,
    "Medium": Medium,
    "Substance": Substance,
    "Particulate": Particulate,
    "Constituent": Constituent,
}

def look_in_cache(name: str | None = None, cache: dict | None = None):
    if name is None or cache is None:
        return None
    return cache[name] if name in cache else None


def get_modules_from(package_name: str) -> list[str]:
    package = importlib.import_module(package_name)
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + ".",
    ):
        modules.append(modname)
    return modules


def load_modules(module = bob, force: bool = False) -> None:
    global class_cache
    global module_cache
    # print(f"Loading modules {module}")
    if force or module.__name__ not in module_cache:
        module_cache[module.__name__] = get_modules_from(module.__name__)


def get_class_from_name(classname: str | None = None, module = bob) -> t.Any:
    global class_cache
    global module_cache
    _super = None
    if not classname:
        raise ValueError("Classname is required")

    _existing = look_in_cache(classname, class_cache)
    if _existing:
        return _existing

    if "." in classname:
        _super, classname = classname.split(".")

        if _super == "UNIT":
            return UNIT[classname]  # type: ignore
        if _super == "Medium":
            return getattr(Medium,classname)  # type: ignore
        if _super == "Substance":
            return getattr(Substance,classname)  # type: ignore
        if _super == "Particulate":
            return getattr(Particulate,classname)  # type: ignore
        if _super == "Constituent":
            return getattr(Constituent,classname)  # type: ignore

    if "|" in classname:
        _module, classname = classname.split("|")
        module = importlib.import_module(_module)  # type: ignore
    load_modules(module)
    for each in module_cache[module.__name__]:
        try:
            submodule = importlib.import_module(f"{each}")
        except ImportError:
            continue
        for name, obj in inspect.getmembers(submodule):
            if (
                isinstance(obj, bob.core.EnumerationKind)
                and "bob.enum" in submodule.__name__
            ):
                _class = getattr(importlib.import_module(f"{submodule.__name__}"), name)
                enum_cache[name] = _class

            if inspect.isclass(obj):
                if name == classname:
                    if _super is not None:
                        _key = f"{_super}.{classname}"
                    else:
                        _key = classname
                    class_cache[_key] = obj
                    return obj  # type: ignore
                if name not in class_cache:
                    class_cache[name] = obj
        if _super is not None:
            if _super in enum_cache:
                _super_class = enum_cache[_super]
                return getattr(_super_class, classname)  # type: ignore
            if classname in enum_cache:
                return enum_cache[classname]  # type: ignore
    raise TypeError(
        f"Class {_super} {classname} not found in {module}, cache is {class_cache}",
    )
