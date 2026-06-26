import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "file_input"


ACTION_PARAMETERS = (
    ("action foo\n    result 1\n", "action_statement(identifier(foo), parameters, suite(result_statement(integer_literal(1))))"),
    ("action foo a\n    result a\n", "action_statement(identifier(foo), parameters(identifier(a)), suite(result_statement(var(identifier(a)))))"),
    ("action foo a b\n    result a + b\n", "action_statement(identifier(foo), parameters(identifier(a), identifier(b)), suite(result_statement(arith_expr(var(identifier(a)), add_operator(+), var(identifier(b))))))"),
    ("action foo a b c\n    result a\n", "action_statement(identifier(foo), parameters(identifier(a), identifier(b), identifier(c)), suite(result_statement(var(identifier(a)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ACTION_PARAMETERS])
@assert_ast_structure(START)
def test_parser_action_parameters(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ACTION_BODY = (
    ('action foo\n    print "hi"\n    result 1\n', 'action_statement(identifier(foo), parameters, suite(builtin_call(builtin_name(print), arguments(string_literal("hi"))), result_statement(integer_literal(1))))'),
)
@pytest.mark.parametrize("source, expected_ast", [*ACTION_BODY])
@assert_ast_structure(START)
def test_parser_action_body(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ACTION_NESTING = (
    ("action outer\n    action inner\n        result 1\n    result call inner\n", "action_statement(identifier(outer), parameters, suite(action_statement(identifier(inner), parameters, suite(result_statement(integer_literal(1)))), result_statement(call_expr(identifier(inner), arguments))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ACTION_NESTING])
@assert_ast_structure(START)
def test_parser_action_nesting(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


CALL_AS_STATEMENT = (
    ("call foo\n", "call_expr(identifier(foo), arguments)"),
    ("call foo 1 2\n", "call_expr(identifier(foo), arguments(integer_literal(1), integer_literal(2)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*CALL_AS_STATEMENT])
@assert_ast_structure(START)
def test_parser_call_as_statement(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ACTION_RECURSION = (
    ("action factorial n\n    if n is 0\n        result 1\n    result n * call factorial n - 1\n",
    "action_statement(identifier(factorial), parameters(identifier(n)), suite(if_statement(comp_expr(var(identifier(n)), comp_operator(is), integer_literal(0)), suite(result_statement(integer_literal(1)))), result_statement(term(var(identifier(n)), mul_operator(*), call_expr(identifier(factorial), arguments(arith_expr(var(identifier(n)), add_operator(-), integer_literal(1))))))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ACTION_RECURSION])
@assert_ast_structure(START)
def test_parser_action_recursion(moon_parser: Lark, source: str, expected_ast: str) -> None: ...