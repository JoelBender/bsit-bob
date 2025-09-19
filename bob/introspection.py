import importlib
import inspect
import pkgutil
import typing as t

import bob

class_cache = {}
module_cache = {}
enum_cache = {}


def look_in_cache(name: str = None, cache: dict = None):
    return cache[name] if name in cache else None


def get_modules_from(package_name: str) -> t.List[str]:
    package = importlib.import_module(package_name)
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        modules.append(modname)
    return modules


def load_modules(module: t.Type = bob, force: bool = False) -> None:
    global class_cache
    global module_cache
    # print(f"Loading modules {module}")
    if force or module.__name__ not in module_cache:
        module_cache[module.__name__] = get_modules_from(module.__name__)


def get_class_from_name(classname: str = None, module: t.Type = bob) -> t.Type:
    global class_cache
    global module_cache
    super = None
    if not classname:
        raise ValueError("Classname is required")

    _existing = look_in_cache(classname, class_cache)
    if _existing:
        return _existing

    if "." in classname:
        super, classname = classname.split(".")
    if "|" in classname:
        _module, classname = classname.split("|")
        module = importlib.import_module(_module)
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
                    if super is not None:
                        _key = f"{super}.{classname}"
                    else:
                        _key = classname
                    class_cache[_key] = obj
                    return obj
                else:
                    if name not in class_cache:
                        class_cache[name] = obj
        if super is not None:
            if super in enum_cache:
                _super_class = enum_cache[super]
                return getattr(_super_class, classname)
            else:
                if classname in enum_cache:
                    return enum_cache[classname]
    raise TypeError(
        f"Class {super} {classname} not found in {module}, cache is {class_cache}"
    )
