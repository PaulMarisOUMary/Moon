from __future__ import annotations

from typing import Any

from lark import Transformer as LTransformer, Token, v_args

from .ast_nodes import (
    FileInput,
    SourceLocation,
    Node,
    Identifier,
    Inheritance,
    Parameters,
    NullLiteral,
    TrueLiteral,
    FalseLiteral,
    IntegerLiteral,
    FloatLiteral,
    StringLiteral,
    Var,
    TernaryExpr,
    CompareExpr,
    BinOp,
    UnaryOp,
    NotExpr,
    CallExpr,
    BuiltinCall,
    MethodCall,
    ListItem,
    ListExpr,
    DictItem,
    DictExpr,
    AssignStatement,
    ListAssignStatement,
    DictAssignStatement,
    StopStatement,
    SkipStatement,
    ResultStatement,
    RaiseStatement,
    NoopStatement,
    WhileStatement,
    IfStatement,
    ElifBranch,
    TestStatement,
    ActionStatement,
    ThingStatement,
    UseName,
    UseFrom,
    UseTarget,
    UseAs,
    DottedPath,
    StarImport,
    Attribute,
)
from .errors import MoonTransformError
from .utils import clean_type


LOC_NODES = frozenset(
    {
        "identifier",
        "var",
        "integer_literal",
        "float_literal",
        "string_literal",
        "true_literal",
        "false_literal",
        "null_literal",
        "assign_statement",
        "list_assign_statement",
        "dict_assign_statement",
        "action_statement",
        "thing_statement",
        "attribute",
        "while_statement",
        "if_statement",
        "test_statement",
        "result_statement",
        "raise_statement",
        "stop_statement",
        "skip_statement",
        "call_expr",
        "method_call",
        "builtin_call",
        "comp_expr",
        "arith_expr",
        "not_expr",
        "factor",
        "power",
        "list_expr",
        "dict_expr",
        "use_name",
        "use_from",
    }
)


class Transformer(LTransformer):
    def __default__(self, data: str, children: list[Any], meta: Any) -> Any:
        raise MoonTransformError(f"Unhandled grammar rule '{data}'")

    def __getattr__(self, name: str) -> Any:
        return super().__getattribute__(clean_type(name))

    def visit_wrapper(self, f: Any, data: str, children: list[Any], meta: Any) -> Any:
        node = f(children)
        if data in LOC_NODES and isinstance(node, Node) and node.loc is None:
            loc = self.meta_loc(meta)
            if loc is not None:
                object.__setattr__(node, "loc", loc)
        return node

    # Helpers

    @staticmethod
    def meta_loc(meta: Any) -> SourceLocation | None:
        line = getattr(meta, "line", None)
        col = getattr(meta, "column", None)
        if line is None or col is None:
            return None
        return SourceLocation(line=line, column=col)

    @staticmethod
    def fold_binop(items: list[Any]) -> Any:
        it = iter(items)
        result = next(it)
        for op, right in zip(it, it):  # Consomme par paires (opérateur, opérande)
            result = BinOp(op=str(op), left=result, right=right)
        return result

    @staticmethod
    def fold_binop_keyword(items: list[Any], op: str) -> Any:
        nodes = [i for i in items if not isinstance(i, Token)]
        if len(nodes) == 1:
            return nodes[0]
        result = nodes[0]
        for operand in nodes[1:]:
            result = BinOp(op=op, left=result, right=operand)
        return result

    # Entry points

    def start(self, items: list[Any]) -> FileInput:
        return items[0]

    def file_input(self, items: list[Any]) -> FileInput:
        return FileInput(body=list(items))

    def single_input(self, items: list[Any]) -> Any:
        return items[0] if items else None

    def eval_input(self, items: list[Any]) -> Any:
        return items[0] if items else None

    # Suites

    def suite(self, items: list[Any]) -> list[Any]:
        return list(items)

    def thing_suite(self, items: list[Any]) -> list[Any]:
        return list(items)

    # Misc

    def identifier(self, items: list[Any]) -> Identifier:
        return Identifier(name=str(items[0]))

    def inheritance(self, items: list[Any]) -> Inheritance:
        ident = next((i for i in items if isinstance(i, Identifier)), None)
        if ident is None:
            raise MoonTransformError("inheritance: expected an Identifier")
        return Inheritance(parent=ident)

    def parameters(self, items: list[Any]) -> Parameters:
        return Parameters(params=list(items))

    def attribute(self, items: list[Any]) -> Attribute:
        return Attribute(name=items[0])

    # Literals

    def null_literal(self, items: list[Any]) -> NullLiteral:
        return NullLiteral()

    def true_literal(self, items: list[Any]) -> TrueLiteral:
        return TrueLiteral()

    def false_literal(self, items: list[Any]) -> FalseLiteral:
        return FalseLiteral()

    def integer_literal(self, items: list[Any]) -> IntegerLiteral:
        return IntegerLiteral(value=int(str(items[0])))

    def float_literal(self, items: list[Any]) -> FloatLiteral:
        return FloatLiteral(value=float(str(items[0])))

    def string_literal(self, items: list[Any]) -> StringLiteral:
        return StringLiteral(value=str(items[0])[1:-1])

    # Expressions

    def var(self, items: list[Any]) -> Var:
        return Var(name=items[0])

    def expression(self, items: list[Any]) -> Any:
        if len(items) == 3:
            then_expr, condition, else_expr = items
            return TernaryExpr(
                condition=condition, then_expr=then_expr, else_expr=else_expr
            )
        return items[0]

    def comp_expr(self, items: list[Any]) -> Any:
        if len(items) == 1:
            return items[0]
        left = items[0]
        operators = []
        operands = []
        i = 1
        while i < len(items):
            operators.append(items[i])
            operands.append(items[i + 1])
            i += 2
        return CompareExpr(left=left, operators=operators, operands=operands)

    @v_args(inline=True)
    def comp_operator(self, op: Token) -> str:
        return str(op)

    def arith_expr(self, items: list[Any]) -> Any:
        return self.fold_binop(items)

    def term(self, items: list[Any]) -> Any:
        return self.fold_binop(items)

    def power(self, items: list[Any]) -> Any:
        if len(items) == 1:
            return items[0]
        base, exp = items
        return BinOp(op="**", left=base, right=exp)

    def factor(self, items: list[Any]) -> Any:
        if len(items) == 1:
            return items[0]
        op, operand = items
        return UnaryOp(op=op, operand=operand)

    @v_args(inline=True)
    def add_operator(self, op: Token) -> str:
        return str(op)

    @v_args(inline=True)
    def mul_operator(self, op: Token) -> str:
        return str(op)

    @v_args(inline=True)
    def unary_operator(self, op: Token) -> str:
        return str(op)

    def or_expr(self, items: list[Any]) -> Any:
        return self.fold_binop_keyword(items, "or")

    def and_expr(self, items: list[Any]) -> Any:
        return self.fold_binop_keyword(items, "and")

    def not_expr(self, items: list[Any]) -> NotExpr:
        return NotExpr(operand=items[0])

    # Calls

    def call_expr(self, items: list[Any]) -> CallExpr:
        return CallExpr(callee=items[0], arguments=items[1])

    def arguments(self, items: list[Any]) -> list[Any]:
        return list(items)

    @v_args(inline=True)
    def builtin_name(self, name: Token) -> str:
        return str(name)

    def builtin_call(self, items: list[Any]) -> BuiltinCall:
        return BuiltinCall(name=items[0], arguments=items[1])

    def method_call(self, items: list[Any]) -> MethodCall:
        return MethodCall(receiver=items[0], method=items[1], arguments=items[2])

    # Collections

    def list_item(self, items: list[Any]) -> ListItem:
        return ListItem(value=items[0])

    def list_expr(self, items: list[Any]) -> ListExpr:
        return ListExpr(items=list(items))

    def dict_item(self, items: list[Any]) -> DictItem:
        return DictItem(key=items[0], value=items[1])

    def dict_expr(self, items: list[Any]) -> DictExpr:
        return DictExpr(items=list(items))

    # Statements

    def assign_statement(self, items: list[Any]) -> AssignStatement:
        name, value = items
        return AssignStatement(name=name, value=value)

    def list_assign_statement(self, items: list[Any]) -> ListAssignStatement:
        name, value = items
        return ListAssignStatement(name=name, value=value)

    def dict_assign_statement(self, items: list[Any]) -> DictAssignStatement:
        name, value = items
        return DictAssignStatement(name=name, value=value)

    def stop_statement(self, items: list[Any]) -> StopStatement:
        return StopStatement()

    def skip_statement(self, items: list[Any]) -> SkipStatement:
        return SkipStatement()

    def noop_statement(self, items: list[Any]) -> NoopStatement:
        return NoopStatement()

    def result_statement(self, items: list[Any]) -> ResultStatement:
        return ResultStatement(value=items[0] if items else None)

    def raise_statement(self, items: list[Any]) -> RaiseStatement:
        return RaiseStatement(value=items[0])

    def while_statement(self, items: list[Any]) -> WhileStatement:
        return WhileStatement(condition=items[0], body=items[1])

    def if_statement(self, items: list[Any]) -> IfStatement:
        condition = items[0]
        then_body = items[1]
        elif_branches = [i for i in items[2:] if isinstance(i, ElifBranch)]
        else_body = next((i for i in items[2:] if isinstance(i, list)), None)
        return IfStatement(
            condition=condition,
            then_body=then_body,
            elif_branches=elif_branches,
            else_body=else_body,
        )

    def elif_branch(self, items: list[Any]) -> ElifBranch:
        return ElifBranch(condition=items[0], body=items[1])

    def test_statement(self, items: list[Any]) -> TestStatement:
        return TestStatement(
            try_body=items[0],
            fail_body=items[1] if len(items) > 1 else None,
        )

    def action_statement(self, items: list[Any]) -> ActionStatement:
        return ActionStatement(name=items[0], parameters=items[1], body=items[2])

    def thing_statement(self, items: list[Any]) -> ThingStatement:
        name = items[0]
        inheritance, body = (
            (items[1], items[2]) if len(items) == 3 else (None, items[1])
        )
        return ThingStatement(name=name, inheritance=inheritance, body=body)

    # Modules

    def use_name(self, items: list[Any]) -> UseName:
        return UseName(name=items[0])

    def use_from(self, items: list[Any]) -> UseFrom:
        source = str(items[0])[1:-1] if isinstance(items[0], Token) else items[0]
        use_target: UseTarget = items[1]
        return UseFrom(source=source, target=use_target.target, alias=use_target.alias)

    def use_as(self, items: list[Any]) -> UseAs:
        return UseAs(alias=items[0])

    def dotted_path(self, items: list[Any]) -> DottedPath:
        return DottedPath(parts=list(items))

    def use_target(self, items: list[Any]) -> UseTarget:
        if (
            len(items) == 1
            and isinstance(items[0], Token)
            and items[0].type == "STAR_IMPORT"
        ):
            return UseTarget(target=StarImport())
        return UseTarget(
            target=items[0],
            alias=items[1] if len(items) > 1 else None,
        )

    def use_statement(self, items: list[Any]) -> UseName | UseFrom:
        return items[0]
