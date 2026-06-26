from __future__ import annotations

from .objects import NULL, Object


class StopSignal(BaseException): ...


class SkipSignal(BaseException): ...


class ResultSignal(BaseException):
    __slots__ = ("value",)

    def __init__(self, value: Object = NULL) -> None:
        self.value = value
