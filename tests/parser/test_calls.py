import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "eval_input"


CALL_EXPRESSIONS = (
    ("call my_func", "call_expr(identifier(my_func), arguments)"),
    ("call run 10", "call_expr(identifier(run), arguments(integer_literal(10)))"),
    ("call run 1 2 3", "call_expr(identifier(run), arguments(integer_literal(1), integer_literal(2), integer_literal(3)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*CALL_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_call_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


BUILTIN_CALL_EXPRESSIONS = (
    ("print", "builtin_call(builtin_name(print), arguments)"),
    ('print "hello"', 'builtin_call(builtin_name(print), arguments(string_literal("hello")))'),
    ("print 1 2 3", "builtin_call(builtin_name(print), arguments(integer_literal(1), integer_literal(2), integer_literal(3)))"),
    ("ask", "builtin_call(builtin_name(ask), arguments)"),
    ('ask "Input: "', 'builtin_call(builtin_name(ask), arguments(string_literal("Input: ")))'),
    ("random", "builtin_call(builtin_name(random), arguments)"),
    ("random 1 10", "builtin_call(builtin_name(random), arguments(integer_literal(1), integer_literal(10)))"),
    ("time", "builtin_call(builtin_name(time), arguments)"),
    ("sleep", "builtin_call(builtin_name(sleep), arguments)"),
    ("sleep 1", "builtin_call(builtin_name(sleep), arguments(integer_literal(1)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*BUILTIN_CALL_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_builtin_call_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


METHOD_CALL_EXPRESSIONS = (
    ("dog bark", "method_call(identifier(dog), identifier(bark), arguments)"),
    ("dog bark loudly", "method_call(identifier(dog), identifier(bark), arguments(var(identifier(loudly))))"),
    ("dog bark 1 2", "method_call(identifier(dog), identifier(bark), arguments(integer_literal(1), integer_literal(2)))"),
)
@pytest.mark.skip(reason="Method call in WIP")
@pytest.mark.parametrize("source, expected_ast", [*METHOD_CALL_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_method_call_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


CALL_ARGUMENT_RESOLUTION_EXPRESSIONS = (
    ("print dog bark", "builtin_call(builtin_name(print), arguments(method_call(identifier(dog), identifier(bark), arguments)))"),
    ("call my_func dog bark", "call_expr(identifier(my_func), arguments(method_call(identifier(dog), identifier(bark), arguments)))"),
)
@pytest.mark.skip(reason="Method call in WIP")
@pytest.mark.parametrize("source, expected_ast", [*CALL_ARGUMENT_RESOLUTION_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_call_argument_resolution(moon_parser: Lark, source: str, expected_ast: str) -> None: ...