from __future__ import annotations

import random as _random_mod
import time as _time_mod
from typing import Any, Callable

from ..errors import MoonTypeError
from .objects import Float, Int, Object, String, NULL


BuiltinFn = Callable[[list[Object], Any], Object]


BUILTINS: dict[str, BuiltinFn] = {}


def _autocast(value: str) -> Object:
    try:
        return Int(int(value))
    except ValueError:
        try:
            return Float(float(value.replace(',', '.')))
        except ValueError:
            return String(value)


def builtin(name: str) -> Callable[[BuiltinFn], BuiltinFn]:
    def decorator(fn: BuiltinFn) -> BuiltinFn:
        BUILTINS[name] = fn
        return fn

    return decorator


@builtin("print")
def _print(args: list[Object], loc: Any) -> Object:
    print(' '.join(repr(a) for a in args))
    return NULL


@builtin("ask")
def _ask(args: list[Object], loc: Any) -> Object:
    prompt = repr(args[0]) if args else ""
    return _autocast(input(prompt))


@builtin("random")
def _random(args: list[Object], loc: Any) -> Object:
    if len(args) == 0:
        return Float(_random_mod.random())
    if len(args) == 2 and isinstance(args[0], Int) and isinstance(args[1], Int):
        return Int(_random_mod.randint(args[0].value, args[1].value))
    raise MoonTypeError("random expects no args or two integers (low, high)", loc=loc)


@builtin("time")
def _time(args: list[Object], loc: Any) -> Object:
    return Float(_time_mod.time())


@builtin("sleep")
def _sleep(args: list[Object], loc: Any) -> Object:
    if not args or not isinstance(args[0], (Int, Float)):
        raise MoonTypeError("sleep expects a number", loc=loc)
    _time_mod.sleep(args[0].value)
    return NULL


# @builtin("exit")
# def _exit(args: list[Object], loc: Any) -> Object:
#     code = args[0].value if args and isinstance(args[0], Int) else 0
#     raise SystemExit(code)
