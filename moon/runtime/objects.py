from __future__ import annotations

from typing import Any

from ..errors import MoonAttributeError
from .environment import Environment


class Object:
    __slots__ = ("cls", "attributes")

    def __init__(self, cls: Thing) -> None:
        self.cls = cls
        self.attributes: dict[str, Object] = {}

    def get_attr(self, name: str) -> Object:
        if name in self.attributes:
            return self.attributes[name]
        return self.cls.find_method(name)

    def set_attr(self, name: str, value: Object) -> None:
        self.attributes[name] = value

    def __repr__(self) -> str:
        return f"<{self.cls.name} object>"


class Thing(Object):
    __slots__ = ("name", "parent", "methods", "attribute_names")

    def __init__(
        self,
        name: str,
        parent: Thing | None,
        attribute_names: list[str] | None = None,
    ) -> None:
        super().__init__(_TYPE_SENTINEL)
        self.name = name
        self.parent = parent
        self.attribute_names: list[str] = (
            attribute_names if attribute_names is not None else []
        )
        self.methods: dict[str, Action] = {}

    def find_method(self, name: str) -> Object:
        if name in self.methods:
            return self.methods[name]
        if self.parent is not None:
            return self.parent.find_method(name)
        raise MoonAttributeError(f"'{self.name}' has no attribute '{name}'")

    def instantiate(self) -> Object:
        instance = Object(self)
        chain: list[Thing] = []
        cls: Thing | None = self
        while cls is not None:
            chain.append(cls)
            cls = cls.parent
        for ancestor in reversed(chain):
            for attr in ancestor.attribute_names:
                instance.attributes[attr] = NULL
        return instance

    def __repr__(self) -> str:
        return f"<class {self.name}>"


_TYPE_SENTINEL: Any = None


class Action(Object):
    __slots__ = ("name", "params", "body", "closure")

    def __init__(
        self,
        name: str,
        params: list[str],
        body: list[Any],
        closure: Environment,
    ) -> None:
        super().__init__(FUNCTION_CLASS)
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self) -> str:
        return f"<action {self.name}>"


class Int(Object):
    __slots__ = ("value",)

    def __init__(self, value: int) -> None:
        super().__init__(INT_CLASS)
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)


class Float(Object):
    __slots__ = ("value",)

    def __init__(self, value: float) -> None:
        super().__init__(FLOAT_CLASS)
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)


class String(Object):
    __slots__ = ("value",)

    def __init__(self, value: str) -> None:
        super().__init__(STRING_CLASS)
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Bool(Object):
    __slots__ = ("value",)

    def __init__(self, value: bool) -> None:
        super().__init__(BOOL_CLASS)
        self.value = value

    def __repr__(self) -> str:
        return "true" if self.value else "false"


class Null(Object):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__(NULL_CLASS)

    def __repr__(self) -> str:
        return "null"


class List(Object):
    __slots__ = ("items",)

    def __init__(self, items: list[Object]) -> None:
        super().__init__(LIST_CLASS)
        self.items = items

    def __repr__(self) -> str:
        return f"[{', '.join(repr(i) for i in self.items)}]"


class Dict(Object):
    __slots__ = ("pairs",)

    def __init__(self, pairs: list[tuple[Object, Object]]) -> None:
        super().__init__(DICT_CLASS)
        self.pairs = pairs

    def get(self, key: Object) -> Object | None:
        for k, v in self.pairs:
            if _obj_values_equal(k, key):
                return v
        return None

    def set(self, key: Object, value: Object) -> None:
        for i, (k, _) in enumerate(self.pairs):
            if _obj_values_equal(k, key):
                self.pairs[i] = (k, value)
                return
        self.pairs.append((key, value))

    def __repr__(self) -> str:
        body = ", ".join(f"{k!r}: {v!r}" for k, v in self.pairs)
        return f"{{{body}}}"


def _obj_values_equal(a: Object, b: Object) -> bool:
    if type(a) is not type(b):
        return False
    if isinstance(a, (Int, Float, String, Bool)):
        return a.value == b.value  # type: ignore
    if isinstance(a, Null):
        return True
    return a is b


_CLASSES: dict[str, Thing] = {}


def _make_object_root() -> Thing:
    root = Thing.__new__(Thing)
    root.name = "Object"
    root.parent = None
    root.methods = {}
    root.attribute_names = []
    root.attributes = {}
    root.cls = root
    _CLASSES["Object"] = root
    return root


def _cls(name: str, parent_name: str | None = "Object") -> Thing:
    parent = _CLASSES[parent_name] if parent_name else None
    cls = Thing(name, parent)
    _CLASSES[name] = cls
    return cls


OBJECT_CLASS = _make_object_root()
TYPE_CLASS = _cls("Type")
NULL_CLASS = _cls("Null")
BOOL_CLASS = _cls("Bool")
INT_CLASS = _cls("Int")
FLOAT_CLASS = _cls("Float")
STRING_CLASS = _cls("String")
LIST_CLASS = _cls("List")
DICT_CLASS = _cls("Dict")
FUNCTION_CLASS = _cls("Function")

OBJECT_CLASS.cls = TYPE_CLASS

NULL = Null()
TRUE = Bool(True)
FALSE = Bool(False)
