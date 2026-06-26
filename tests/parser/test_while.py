import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "file_input"


WHILE_STATEMENTS = (
    ("while true\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("while x < 10\n    x is x + 1\n", "while_statement(comp_expr(var(identifier(x)), comp_operator(<), integer_literal(10)), suite(assign_statement(identifier(x), is, arith_expr(var(identifier(x)), add_operator(+), integer_literal(1)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*WHILE_STATEMENTS])
@assert_ast_structure(START)
def test_parser_while_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


WHILE_MULTI_STATEMENT_BODY = (
    ("while true\n    print 1\n    print 2\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1))), builtin_call(builtin_name(print), arguments(integer_literal(2)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*WHILE_MULTI_STATEMENT_BODY])
@assert_ast_structure(START)
def test_parser_while_multi_statement_body(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


WHILE_NESTING = (
    ("while true\n    while false\n        print 1\n", "while_statement(true_literal, suite(while_statement(false_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*WHILE_NESTING])
@assert_ast_structure(START)
def test_parser_while_nesting(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


WHILE_WITH_CONTROL_FLOW = (
    ("while true\n    stop\n", "while_statement(true_literal, suite(stop_statement))"),
    ("while true\n    skip\n", "while_statement(true_literal, suite(skip_statement))"),
    ("while true\n    if x\n        skip\n    stop\n", "while_statement(true_literal, suite(if_statement(var(identifier(x)), suite(skip_statement)), stop_statement))"),
)
@pytest.mark.parametrize("source, expected_ast", [*WHILE_WITH_CONTROL_FLOW])
@assert_ast_structure(START)
def test_parser_while_with_control_flow(moon_parser: Lark, source: str, expected_ast: str) -> None: ...