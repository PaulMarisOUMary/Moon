from __future__ import annotations

from .parser import parse
from .transformer import Transformer
from .runtime import NULL
from .runtime.interpreter import Interpreter
from .runtime.objects import Object


_transformer = Transformer()


_transformer = Transformer()


class Session:
    def __init__(self) -> None:
        self._interp = Interpreter()

    def _compile(self, source: str):
        return _transformer.transform(parse(source))

    def run(self, source: str) -> None:
        self._interp.run(self._compile(source))

    def eval_expr(self, source: str) -> Object:
        ast = self._compile(source)
        result = NULL
        for node in ast.body:
            result = self._interp.eval_expr(node, self._interp._global)
        return result


def run(source: str) -> None:
    Session().run(source)


def eval_expr(source: str) -> Object:
    return Session().eval_expr(source)
