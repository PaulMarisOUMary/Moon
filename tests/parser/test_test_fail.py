import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


TEST_ONLY = (
    (
        "test\n    x is 1\n",
        "test_statement(suite(assign_statement(identifier(x), is, integer_literal(1))))",
    ),
    (
        "test\n    x is call foo\n",
        "test_statement(suite(assign_statement(identifier(x), is, call_expr(identifier(foo), arguments))))",
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*TEST_ONLY])
@assert_ast_structure(START)
def test_parser_test_only(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


TEST_WITH_FAIL = (
    (
        'test\n    x is 1\nfail\n    print "error"\n',
        'test_statement(suite(assign_statement(identifier(x), is, integer_literal(1))), suite(builtin_call(builtin_name(print), arguments(string_literal("error")))))',
    ),
    (
        'test\n    raise "oops"\nfail\n    print "caught"\n',
        'test_statement(suite(raise_statement(string_literal("oops"))), suite(builtin_call(builtin_name(print), arguments(string_literal("caught")))))',
    ),
    (
        "test\n    x is call foo\nfail\n    x is 0\n",
        "test_statement(suite(assign_statement(identifier(x), is, call_expr(identifier(foo), arguments))), suite(assign_statement(identifier(x), is, integer_literal(0))))",
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*TEST_WITH_FAIL])
@assert_ast_structure(START)
def test_parser_test_with_fail(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


FAIL_WITHOUT_TEST_INVALID = (
    "fail\n    print 1\n",
)
@pytest.mark.parametrize("source", [*FAIL_WITHOUT_TEST_INVALID])
@assert_parse_error(START)
def test_parser_fail_without_test_invalid(moon_parser: Lark, source: str) -> None: ...