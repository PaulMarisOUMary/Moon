from __future__ import annotations

from .objects import Bool, Dict, Float, Int, List, Null, Object, String, FALSE, TRUE


def is_truthy(obj: Object) -> bool:
    match obj:
        case Null():
            return False
        case Bool(value=v):
            return v
        case Int(value=v):
            return v != 0
        case Float(value=v):
            return v != 0.0
        case String(value=v):
            return bool(v)
        case List(items=items):
            return bool(items)
        case Dict(pairs=pairs):
            return bool(pairs)
        case _:
            return True


def moon_bool(value: bool) -> Bool:
    return TRUE if value else FALSE
