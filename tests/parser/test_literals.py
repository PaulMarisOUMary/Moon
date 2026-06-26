import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "eval_input"


BOOLEAN_AND_NULL_LITERAL = (
    ("true", "true_literal"),
    ("false", "false_literal"),
    ("null", "null_literal"),
)
@pytest.mark.parametrize("source, expected_ast", [*BOOLEAN_AND_NULL_LITERAL])
@assert_ast_structure(START)
def test_parser_boolean_and_null(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


INTEGER_LITERAL = (
    ('0', "integer_literal(0)"),
    ('1', "integer_literal(1)"),
    ("42", "integer_literal(42)"),
    ("4096", "integer_literal(4096)"),
    ("-0", "integer_literal(-0)"),
    ("-1", "integer_literal(-1)"),
    ("-42", "integer_literal(-42)"),
    ("-4096", "integer_literal(-4096)"),
    ("+0", "integer_literal(+0)"),
    ("+1", "integer_literal(+1)"),
    ("+42", "integer_literal(+42)"),
    ("+4096", "integer_literal(+4096)"),
)
@pytest.mark.parametrize("source, expected_ast", [*INTEGER_LITERAL])
@assert_ast_structure(START)
def test_parser_integer_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


FLOAT_LITERAL = (
    ("0.0", "float_literal(0.0)"),
    ("0.00000000", "float_literal(0.00000000)"),
    ("1.1", "float_literal(1.1)"),
    (".0001", "float_literal(.0001)"),
    ("1e10", "float_literal(1e10)"),
    ("1E10", "float_literal(1E10)"),
    ("1e-10", "float_literal(1e-10)"),
    ("1E-10", "float_literal(1E-10)"),
    ("1e+10", "float_literal(1e+10)"),
    ("1E+10", "float_literal(1E+10)"),
    (".1e10", "float_literal(.1e10)"),
    (".1E10", "float_literal(.1E10)"),
    (".1e-10", "float_literal(.1e-10)"),
    (".1E-10", "float_literal(.1E-10)"),
    (".1e+10", "float_literal(.1e+10)"),
    (".1E+10", "float_literal(.1E+10)"),
    ("-0.0", "float_literal(-0.0)"),
    ("-0.00000000", "float_literal(-0.00000000)"),
    ("-1.1", "float_literal(-1.1)"),
    ("-.0001", "float_literal(-.0001)"),
    ("-1e10", "float_literal(-1e10)"),
    ("-1E10", "float_literal(-1E10)"),
    ("-1e-10", "float_literal(-1e-10)"),
    ("-1E-10", "float_literal(-1E-10)"),
    ("-1e+10", "float_literal(-1e+10)"),
    ("-1E+10", "float_literal(-1E+10)"),
    ("-.1e10", "float_literal(-.1e10)"),
    ("-.1E10", "float_literal(-.1E10)"),
    ("-.1e-10", "float_literal(-.1e-10)"),
    ("-.1E-10", "float_literal(-.1E-10)"),
    ("-.1e+10", "float_literal(-.1e+10)"),
    ("-.1E+10", "float_literal(-.1E+10)"),
    ("+0.0", "float_literal(+0.0)"),
    ("+0.00000000", "float_literal(+0.00000000)"),
    ("+1.1", "float_literal(+1.1)"),
    ("+.0001", "float_literal(+.0001)"),
    ("+1e10", "float_literal(+1e10)"),
    ("+1E10", "float_literal(+1E10)"),
    ("+1e-10", "float_literal(+1e-10)"),
    ("+1E-10", "float_literal(+1E-10)"),
    ("+1e+10", "float_literal(+1e+10)"),
    ("+1E+10", "float_literal(+1E+10)"),
    ("+.1e10", "float_literal(+.1e10)"),
    ("+.1E10", "float_literal(+.1E10)"),
    ("+.1e-10", "float_literal(+.1e-10)"),
    ("+.1E-10", "float_literal(+.1E-10)"),
    ("+.1e+10", "float_literal(+.1e+10)"),
    ("+.1E+10", "float_literal(+.1E+10)"),
)
@pytest.mark.parametrize("source, expected_ast", [*FLOAT_LITERAL])
@assert_ast_structure(START)
def test_parser_float_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


STRING_LITERAL = (
    ('"string"', 'string_literal("string")'),
    ('""', 'string_literal("")'),
    ('"string with spaces"', 'string_literal("string with spaces")'),
    ('"string with (parens) {} []"', 'string_literal("string with (parens) {} []")'),
    ('"string with \\"quotes\\""', 'string_literal("string with \\"quotes\\"")'),
    ('"string with \\\\ backslash"', 'string_literal("string with \\\\ backslash")'),
    ('"string with \\n new line"', 'string_literal("string with \\n new line")'),
    ('"string with \\t tabulation"', 'string_literal("string with \\t tabulation")'),
    ('"string with \\u2600 unicode"', 'string_literal("string with \\u2600 unicode")'),
    ('"emoji 🍎"', 'string_literal("emoji 🍎")'),
    ("'string'", "string_literal('string')"),
    ("'string\\\\'", "string_literal('string\\\\')"),
    ("''", "string_literal('')"),
    ("'string with spaces'", "string_literal('string with spaces')"),
    ("'string with (parens) {} []'", "string_literal('string with (parens) {} []')"),
    ("'string with \\'quotes\\''", "string_literal('string with \\'quotes\\'')"),
    ("'string with \\\\ backslash'", "string_literal('string with \\\\ backslash')"),
    ("'string with \\n new line'", "string_literal('string with \\n new line')"),
    ("'string with \\t tabulation'", "string_literal('string with \\t tabulation')"),
    ("'string with \\u2600 unicode'", "string_literal('string with \\u2600 unicode')"),
    ("'emoji 🍎'", "string_literal('emoji 🍎')"),
)
@pytest.mark.parametrize("source, expected_ast", [*STRING_LITERAL])
@assert_ast_structure(START)
def test_parser_string_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...