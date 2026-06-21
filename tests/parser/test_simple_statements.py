import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


LOOP_CONTROL_STATEMENTS = (
    ("stop", "stop_statement"),
    ("skip", "skip_statement"),
)
@pytest.mark.parametrize("source, expected_ast", [*LOOP_CONTROL_STATEMENTS])
@assert_ast_structure(START)
def test_parser_loop_control_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


RESULT_STATEMENTS = (
    ("result", "result_statement"),
    ("result 5", "result_statement(integer_literal(5))"),
    ("result true", "result_statement(true_literal)"),
    ("result null", "result_statement(null_literal)"),
    ("result x", "result_statement(var(identifier(x)))"),
    ("result x + 1", "result_statement(arith_expr(var(identifier(x)), add_operator(+), integer_literal(1)))"),
    ("result call my_func", "result_statement(call_expr(identifier(my_func), arguments))"),
)
@pytest.mark.parametrize("source, expected_ast", [*RESULT_STATEMENTS])
@assert_ast_structure(START)
def test_parser_result_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


RAISE_STATEMENTS = (
    ('raise "error"', 'raise_statement(string_literal("error"))'),
    ("raise x", "raise_statement(var(identifier(x)))"),
    ("raise 42", "raise_statement(integer_literal(42))"),
)
@pytest.mark.parametrize("source, expected_ast", [*RAISE_STATEMENTS])
@assert_ast_structure(START)
def test_parser_raise_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


RAISE_STATEMENT_INVALID = (
    "raise",
)
@pytest.mark.parametrize("source", [*RAISE_STATEMENT_INVALID])
@assert_parse_error(START)
def test_parser_raise_statement_requires_expression(moon_parser: Lark, source: str) -> None: ...


NOOP_STATEMENTS = (
    ("...", "noop_statement"),
)
@pytest.mark.parametrize("source, expected_ast", [*NOOP_STATEMENTS])
@assert_ast_structure(START)
def test_parser_noop_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...