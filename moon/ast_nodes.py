from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int
    source: str = ''

    def __str__(self) -> str:
        prefix = f"{self.source}:" if self.source else ''
        return f"{prefix}{self.line}:{self.column}"


@dataclass(slots=True)
class Node:
    loc: SourceLocation | None = field(default=None, repr=False, compare=False)


# Misc


@dataclass(slots=True)
class Identifier(Node):
    name: str = ''

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or self.name == '':
            raise ValueError("Identifier.name must be a non-empty string")


@dataclass(slots=True)
class Inheritance(Node):
    parent: Identifier = field(default_factory=Identifier)


@dataclass(slots=True)
class Parameters(Node):
    params: list[Identifier] = field(default_factory=list)


# Literals


@dataclass(slots=True)
class NullLiteral(Node): ...


@dataclass(slots=True)
class TrueLiteral(Node): ...


@dataclass(slots=True)
class FalseLiteral(Node): ...


@dataclass(slots=True)
class IntegerLiteral(Node):
    value: int = 0

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError(
                f"IntegerLiteral.value must be int, got {type(self.value).__name__}"
            )


@dataclass(slots=True)
class FloatLiteral(Node):
    value: float = 0.0

    def __post_init__(self):
        if not isinstance(self.value, float):
            raise TypeError(
                f"FloatLiteral.value must be float, got {type(self.value).__name__}"
            )


@dataclass(slots=True)
class StringLiteral(Node):
    value: str = ''


# Expressions


@dataclass(slots=True)
class Var(Node):
    name: Identifier = field(default_factory=Identifier)


@dataclass(slots=True)
class TernaryExpr(Node):
    condition: Any = None
    then_expr: Any = None
    else_expr: Any = None


@dataclass(slots=True)
class CompareExpr(Node):
    left: Any = None
    operators: list[str] = field(default_factory=list)
    operands: list[Any] = field(default_factory=list)

    def __post_init__(self):
        if len(self.operators) != len(self.operands):
            raise ValueError(
                f"CompareExpr: operators({len(self.operators)}) "
                f"and operands({len(self.operands)}) must have the same length"
            )


@dataclass(slots=True)
class BinOp(Node):
    op: str = ''
    left: Any = None
    right: Any = None


@dataclass(slots=True)
class UnaryOp(Node):
    op: str = ''
    operand: Any = None


@dataclass(slots=True)
class NotExpr(Node):
    operand: Any = None


@dataclass(slots=True)
class CallExpr(Node):
    callee: Identifier = field(default_factory=Identifier)
    arguments: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class BuiltinCall(Node):
    name: str = ''
    arguments: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class MethodCall(Node):
    receiver: Identifier = field(default_factory=Identifier)
    method: Identifier = field(default_factory=Identifier)
    arguments: list[Any] = field(default_factory=list)


# Collections


@dataclass(slots=True)
class ListItem(Node):
    value: Any = None


@dataclass(slots=True)
class ListExpr(Node):
    items: list[ListItem] = field(default_factory=list)


@dataclass(slots=True)
class DictItem(Node):
    key: Any = None
    value: Any = None


@dataclass(slots=True)
class DictExpr(Node):
    items: list[DictItem] = field(default_factory=list)


# Statements


@dataclass(slots=True)
class FileInput(Node):
    body: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class AssignStatement(Node):
    name: Identifier = field(default_factory=Identifier)
    value: Any = None


@dataclass(slots=True)
class ListAssignStatement(Node):
    name: Identifier = field(default_factory=Identifier)
    value: ListExpr = field(default_factory=ListExpr)


@dataclass(slots=True)
class DictAssignStatement(Node):
    name: Identifier = field(default_factory=Identifier)
    value: DictExpr = field(default_factory=DictExpr)


@dataclass(slots=True)
class StopStatement(Node): ...


@dataclass(slots=True)
class SkipStatement(Node): ...


@dataclass(slots=True)
class ResultStatement(Node):
    value: Any | None = None


@dataclass(slots=True)
class RaiseStatement(Node):
    value: Any = None


@dataclass(slots=True)
class NoopStatement(Node): ...


@dataclass(slots=True)
class WhileStatement(Node):
    condition: Any = None
    body: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class ElifBranch(Node):
    condition: Any = None
    body: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class IfStatement(Node):
    condition: Any = None
    then_body: list[Any] = field(default_factory=list)
    elif_branches: list[ElifBranch] = field(default_factory=list)
    else_body: list[Any] | None = None


@dataclass(slots=True)
class TestStatement(Node):
    try_body: list[Any] = field(default_factory=list)
    fail_body: list[Any] | None = None


@dataclass(slots=True)
class Attribute(Node):
    name: Identifier = field(default_factory=Identifier)


@dataclass(slots=True)
class ActionStatement(Node):
    name: Identifier = field(default_factory=Identifier)
    parameters: Parameters = field(default_factory=Parameters)
    body: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class ThingStatement(Node):
    name: Identifier = field(default_factory=Identifier)
    inheritance: Inheritance | None = None
    body: list[Any] = field(default_factory=list)


# Modules


@dataclass(slots=True)
class DottedPath(Node):
    parts: list[Identifier] = field(default_factory=list)


@dataclass(slots=True)
class UseAs(Node):
    alias: Identifier = field(default_factory=Identifier)


@dataclass(slots=True)
class StarImport(Node): ...


@dataclass(slots=True)
class UseTarget(Node):
    target: Identifier | StarImport = field(default_factory=StarImport)
    alias: UseAs | None = None


@dataclass(slots=True)
class UseName(Node):
    name: Identifier = field(default_factory=Identifier)


@dataclass(slots=True)
class UseFrom(Node):
    source: str | DottedPath | None = None
    target: Identifier | StarImport = field(default_factory=Identifier)
    alias: UseAs | None = None


Literal = (
    NullLiteral
    | TrueLiteral
    | FalseLiteral
    | IntegerLiteral
    | FloatLiteral
    | StringLiteral
)


Statement = (
    AssignStatement
    | ListAssignStatement
    | DictAssignStatement
    | StopStatement
    | SkipStatement
    | ResultStatement
    | RaiseStatement
    | NoopStatement
    | WhileStatement
    | IfStatement
    | TestStatement
    | ActionStatement
    | ThingStatement
    | UseName
    | UseFrom
)


Expression = (
    Var
    | TernaryExpr
    | CompareExpr
    | BinOp
    | UnaryOp
    | NotExpr
    | CallExpr
    | BuiltinCall
    | MethodCall
    | ListExpr
    | DictExpr
    | Literal
)