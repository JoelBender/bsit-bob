# multimethods
#
# This is a re-work of multimethods from Eli Bendersky
# [http://eli.thegreenplace.net] who placed it the public domain.  This
# derivative is also in the public domain.
#

from __future__ import annotations

import inspect
import itertools
import logging
from collections import Counter
from typing import Any, Callable, Dict, List, Set, Tuple, Union, get_origin

__all__ = ["multimethod"]


# logging
_log = logging.getLogger("multimethods")
_log.addHandler(logging.NullHandler())

# Maps function.__name__ -> _MultiMethod object.
_multi_registry: Dict[str, _MultiMethod] = {}


class _MultiMethod:
    """Maps tuples of argument types to function to call for these types."""

    name: str
    argc: int
    types: Set[type]
    typemap: Dict[Tuple[type, ...], Callable[..., Any]]
    funcs: List[Callable[..., Any]]
    invocations: Counter

    def __init__(self, name: str) -> None:
        self.name = name
        self.types = set()
        self.typemap = {}
        self.funcs = []
        self.invocations = Counter()
        self.argc = -1

    def __call__(self, *args: Any) -> Any:
        _log.debug("(%s)__call__: %r", self.name, args)

        # if the typemap is empty it hasn't been populated yet
        if not self.typemap:
            self.populate_typemap()

        types = list(arg.__class__ for arg in args)

        # pad the list of types with None if there aren't enough
        if len(types) > self.argc:
            raise RuntimeError(f"too many parameters, expecting {self.argc}")
        elif len(types) < self.argc:
            types.extend([type(None)] * (self.argc - len(types)))
        _log.debug("    - types: %r", types)

        if list in types:
            for i, arg_type in enumerate(types):
                if arg_type is list:
                    parm_subtypes = set(elem.__class__ for elem in args[i])

                    # make an ordered dict of the first subtype __mro__
                    top_mro = {s: None for s in parm_subtypes.pop().__mro__}

                    # keep the classes in the top_mro that are in each of
                    # the other parm_subtypes __mro__
                    for cls in parm_subtypes:
                        top_mro = {s: None for s in top_mro if s in cls.__mro__}

                    types[i] = List[next(iter(top_mro))]  # type: ignore[index,misc]

        types_tuple = tuple(types)
        _log.debug("    - types_tuple: %r", types_tuple)

        method = self.typemap.get(types_tuple, None)
        if not method:
            raise TypeError("no match %r: %s" % (self.name, types))

        # found a match, count it
        self.invocations[(types_tuple, method)] += 1

        return method(*args)

    def register_function(self, func: Callable[..., Any]) -> None:
        _log.debug("(%s)register_function: %r", self.name, func)

        if self.typemap:
            _log.warning("forcing repopulatation: %r", self)

            # clear out the existing map for now
            self.types = set()
            self.typemap = {}

        # get the function signature to make sure the same number of parameters
        # is used every time.
        func_sig = inspect.signature(func)
        argc = len(func_sig.parameters)
        if self.argc < 0:
            self.argc = argc
        elif argc != self.argc:
            raise RuntimeError(f"expecting {self.argc} parameters, got {argc}")

        # add the function for the population step
        self.funcs.append(func)

    def populate_typemap(self):
        _log.debug("(%s)populate_typemap", self.name)

        # clear out the existing map
        self.types = set()
        self.typemap = {}

        # map each function in the order it was registered
        for func in self.funcs:
            types_with_subclasses = []

            func_sig = inspect.signature(func)
            for parameter in func_sig.parameters.values():
                parm_type = parameter.annotation
                if isinstance(parm_type, str):
                    parm_type = eval(parm_type, func.__globals__)
                parm_origin = get_origin(parm_type)

                if inspect.isclass(parm_type):
                    types_with_subclasses.append(
                        [parm_type] + all_subclasses(parm_type)
                    )

                elif parm_origin is Union:
                    parm_types = set()
                    for parm_subtype in parm_type.__args__:
                        if not inspect.isclass(parm_subtype):
                            raise TypeError(
                                f"parameter {parameter.name} subtype: {parm_subtype!r}"
                            )
                        parm_types.add(parm_subtype)
                        parm_types.update(all_subclasses(parm_subtype))

                    types_with_subclasses.append(parm_types)

                elif parm_origin is list:
                    parm_subtype = parm_type.__args__[0]
                    if not inspect.isclass(parm_subtype):
                        raise TypeError(
                            f"parameter {parameter.name} subtype: {parm_subtype!r}"
                        )

                    parm_types = set([List[parm_subtype]])
                    for more_subtypes in all_subclasses(parm_subtype):
                        parm_types.add(List[more_subtypes])

                    types_with_subclasses.append(parm_types)

                else:
                    raise TypeError(
                        f"parameter {parameter.name}: {parm_type!r} {parm_origin!r}"
                    )

            for type_tuple in itertools.product(*types_with_subclasses):
                # Here we explicitly support overriding the registration, so that
                # more specific dispatches can override earlier-defined generic
                # dispatches.
                self.typemap[type_tuple] = func
                self.types.update(type_tuple)

        # if there are any existing invocations, see if they might change
        for types_tuple, method in self.invocations:
            _log.debug("    - make sure %s still calls %r", types_tuple, method)

            if types_tuple not in self.typemap:
                raise RuntimeError(
                    "%s previous calls no longer mapped: %s", self.name, types_tuple
                )
            if self.typemap[types_tuple] is not method:
                raise RuntimeError(
                    "%s previous calls new method: %s", self.name, types_tuple
                )


def multimethod(func: Callable[..., Any]) -> _MultiMethod:
    """Function Decorator"""
    _log.debug("multimethod %r", func)

    name = func.__name__
    mm = _multi_registry.get(name)
    if mm is None:
        mm = _multi_registry[name] = _MultiMethod(name)
    mm.register_function(func)
    return mm


def all_subclasses(cls: type) -> List[type]:
    """Returns a list of *all* subclasses of cls, recursively."""
    if not hasattr(cls, "__subclasses__"):
        return []

    subclasses: List[type] = cls.__subclasses__()
    for subcls in cls.__subclasses__():
        subclasses.extend(all_subclasses(subcls))
    return subclasses


def new_class(cls: type) -> None:
    _log.debug("new_class %r", cls.__name__)

    # check to see if the new type is a subclass of an existing type
    for fn_name, mm in _multi_registry.items():
        ding = False
        for mm_type in mm.types:
            if inspect.isclass(mm_type):
                if issubclass(cls, mm_type):
                    _log.debug(
                        "    - %s ding: %r is a subclass of %r", fn_name, cls, mm_type
                    )
                    ding = True
                    break
                continue

            mm_origin = get_origin(mm_type)
            if mm_origin is list:
                mm_subtype = mm_type.__args__[0]  # type: ignore[attr-defined]
                if issubclass(cls, mm_subtype):
                    _log.debug(
                        "    - %s ding: %r is a subclass of %r",
                        fn_name,
                        cls,
                        mm_subtype,
                    )
                    ding = True
                    break
                continue

        if ding:
            # clear out the existing map for now
            mm.types = set()
            mm.typemap = {}
