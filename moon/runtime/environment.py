from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import MoonNameError

if TYPE_CHECKING:
    from .objects import Object


class Environment:
    __slots__ = ("_store", "_parent")

    def __init__(self, parent: Environment | None = None) -> None:
        self._parent = parent
        self._store: dict[str, Object] = {}

    def get(self, name: str) -> Object:
        if name in self._store:
            return self._store[name]
        if self._parent is not None:
            return self._parent.get(name)
        raise MoonNameError(f"'{name}' is not defined")

    def set(self, name: str, value: Object) -> None:
        self._store[name] = value

    def child(self) -> Environment:
        return Environment(parent=self)

    def __contains__(self, name: str) -> bool:
        if name in self._store:
            return True
        if self._parent is not None:
            return name in self._parent
        return False

    def __repr__(self) -> str:
        return (
            f"Environment({list(self._store)!r}, "
            f"parent={'yes' if self._parent else 'no'})"
        )
