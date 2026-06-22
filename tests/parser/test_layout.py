import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "file_input"


LINE_CONT_EXPRESSIONS = (
    (
        "x is 1 +\\\n    2\n",
        "assign_statement(identifier(x), is, arith_expr(integer_literal(1), add_operator(+), integer_literal(2)))",
    ),
    (
        "x is true and\\\n    false\n",
        "assign_statement(identifier(x), is, and_expr(true_literal, and, false_literal))",
    ),
    (
        'print "hello" \\\n    "world"\n',
        'builtin_call(builtin_name(print), arguments(string_literal("hello"), string_literal("world")))',
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*LINE_CONT_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_line_cont_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...