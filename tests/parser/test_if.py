import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


IF_ONLY = (
    ("if true\n    print 1\n", "if_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*IF_ONLY])
@assert_ast_structure(START)
def test_parser_if_only(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


IF_ELSE = (
    ("if true\n    print 1\nelse\n    print 2\n", "if_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))), suite(builtin_call(builtin_name(print), arguments(integer_literal(2)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*IF_ELSE])
@assert_ast_structure(START)
def test_parser_if_else(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


IF_ELIF = (
    ("if a\n    x is 1\nelif b\n    x is 2\n", "if_statement(var(identifier(a)), suite(assign_statement(identifier(x), is, integer_literal(1))), elif_branch(var(identifier(b)), suite(assign_statement(identifier(x), is, integer_literal(2)))))"),
    ("if a\n    x is 1\nelif b\n    x is 2\nelse\n    x is 3\n", "if_statement(var(identifier(a)), suite(assign_statement(identifier(x), is, integer_literal(1))), elif_branch(var(identifier(b)), suite(assign_statement(identifier(x), is, integer_literal(2)))), suite(assign_statement(identifier(x), is, integer_literal(3))))"),
    ("if a\n    x is 1\nelif b\n    x is 2\nelif c\n    x is 3\nelse\n    x is 4\n", "if_statement(var(identifier(a)), suite(assign_statement(identifier(x), is, integer_literal(1))), elif_branch(var(identifier(b)), suite(assign_statement(identifier(x), is, integer_literal(2)))), elif_branch(var(identifier(c)), suite(assign_statement(identifier(x), is, integer_literal(3)))), suite(assign_statement(identifier(x), is, integer_literal(4))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*IF_ELIF])
@assert_ast_structure(START)
def test_parser_if_elif(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


IF_NESTING = (
    ("if a\n    if b\n        x is 1\n", "if_statement(var(identifier(a)), suite(if_statement(var(identifier(b)), suite(assign_statement(identifier(x), is, integer_literal(1))))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*IF_NESTING])
@assert_ast_structure(START)
def test_parser_if_nesting(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


IF_ELIF_AFTER_ELSE_INVALID = (
    "if a\n    x is 1\nelse\n    x is 2\nelif b\n    x is 3\n",
)
@pytest.mark.parametrize("source", [*IF_ELIF_AFTER_ELSE_INVALID])
@assert_parse_error(START)
def test_parser_if_elif_after_else_invalid(moon_parser: Lark, source: str) -> None: ...