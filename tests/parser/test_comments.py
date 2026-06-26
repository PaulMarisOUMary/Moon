import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


COMMENT_TRANSPARENCY = (
    ("# leading comment\nx is 5\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("x is 5  # trailing comment\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("x is 5#no space before hash\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("# c1\n# c2\n# c3\nx is 5\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("while true\n    # comment\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*COMMENT_TRANSPARENCY])
@assert_ast_structure(START)
def test_parser_comment_transparency(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


BLOCK_COMMENT_TRANSPARENCY = (
    ("(\n    Title\n    description\n)\nx is 1\n", "assign_statement(identifier(x), is, integer_literal(1))"),
    ("x is 5 (trailing note)\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("x is (note before value) 5\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("while true\n    (note) print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("x is (a\nmulti-line\nnote) 5\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("while true\n    print 1\n(note between statements)\nx is 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1))))), assign_statement(identifier(x), is, integer_literal(1))"),
)
@pytest.mark.parametrize("source, expected_ast", [*BLOCK_COMMENT_TRANSPARENCY])
@assert_ast_structure(START)
def test_parser_block_comment_transparency(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


BLOCK_COMMENT_STANDALONE_IN_SUITE = (
    ("while true\n    (note)\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("while true\n    print 1\n    (note)\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("while true\n    print 1\n    (note)\n    print 2\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1))), builtin_call(builtin_name(print), arguments(integer_literal(2)))))"),
    ("while true\n    (a)\n    (b)\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("while true\n    (\n        a longer\n        explanation\n    )\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*BLOCK_COMMENT_STANDALONE_IN_SUITE])
@assert_ast_structure(START)
def test_parser_block_comment_standalone_in_suite(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


SUITE_REQUIRES_A_REAL_STATEMENT = (
    "while true\n\n",
    "while true\n    (note)\n",
    "while true\n    # comment\n",
)
@pytest.mark.parametrize("source", [*SUITE_REQUIRES_A_REAL_STATEMENT])
@assert_parse_error(START)
def test_parser_suite_requires_a_real_statement(moon_parser: Lark, source: str) -> None: ...


BLOCK_COMMENT_NESTED_PARENS_LIMITATION = (
    "(this has (nested) parens)\nx is 1\n",
)
@pytest.mark.parametrize("source", [*BLOCK_COMMENT_NESTED_PARENS_LIMITATION])
@assert_parse_error(START)
def test_parser_block_comment_nested_parens_limitation(moon_parser: Lark, source: str) -> None: ...