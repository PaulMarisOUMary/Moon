from .ast_nodes import SourceLocation


class MoonError(Exception):
    def __init__(self, message: str, loc: SourceLocation | None = None) -> None:
        self.loc = loc
        prefix = f"[{loc}]" if loc else ''
        super().__init__(f"{prefix}{message}")


# Transformer

class MoonTransformError(MoonError): ...


# Interpreter

class MoonRuntimeError(MoonError): ...


class MoonNameError(MoonRuntimeError): ...


class MoonTypeError(MoonRuntimeError): ...


class MoonAttributeError(MoonRuntimeError): ...


class MoonArithmeticError(MoonRuntimeError): ...


class MoonUserError(MoonRuntimeError): ...
