import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "file_input"

ASSIGN_STATEMENT_SCALAR = (
    ("x is 5", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("x is 1.5", "assign_statement(identifier(x), is, float_literal(1.5))"),
    ("x is true", "assign_statement(identifier(x), is, true_literal)"),
    ("x is false", "assign_statement(identifier(x), is, false_literal)"),
    ("x is null", "assign_statement(identifier(x), is, null_literal)"),
    ('x is "hello"', 'assign_statement(identifier(x), is, string_literal("hello"))'),
    ("x is y", "assign_statement(identifier(x), is, var(identifier(y)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ASSIGN_STATEMENT_SCALAR])
@assert_ast_structure(START)
def test_parser_assign_statement_scalar(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ASSIGN_STATEMENT_EXPRESSION = (
    ("x is 1 + 2", "assign_statement(identifier(x), is, arith_expr(integer_literal(1), add_operator(+), integer_literal(2)))"),
    ("x is not true", "assign_statement(identifier(x), is, not_expr(not, true_literal))"),
    ("x is y if true else z", "assign_statement(identifier(x), is, expression(var(identifier(y)), true_literal, var(identifier(z))))"),
    ("x is call my_func", "assign_statement(identifier(x), is, call_expr(identifier(my_func), arguments))"),
    ("x is print 1", "assign_statement(identifier(x), is, builtin_call(builtin_name(print), arguments(integer_literal(1))))"),
    ("x is dog bark", "assign_statement(identifier(x), is, method_call(identifier(dog), identifier(bark), arguments))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ASSIGN_STATEMENT_EXPRESSION])
@assert_ast_structure(START)
def test_parser_assign_statement_expression(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ASSIGN_STATEMENT_REASSIGNMENT = (
    ("x is 1\nx is 2\n", "assign_statement(identifier(x), is, integer_literal(1)), assign_statement(identifier(x), is, integer_literal(2))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ASSIGN_STATEMENT_REASSIGNMENT])
@assert_ast_structure(START)
def test_parser_assign_statement_reassignment(moon_parser: Lark, source: str, expected_ast: str) -> None: ...