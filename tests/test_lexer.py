import pytest

from functools import wraps
from typing import Any, Callable, Optional

from lark import Lark
from lark.exceptions import UnexpectedCharacters


def clean_type(token_type: str) -> str:
    return token_type.split("__")[-1]


def assert_single_token(func: Callable[..., None]) -> Callable[..., None]:
    @wraps(func)
    def wrapper(moon_parser: Lark, source: str, *args: Any, **kwargs: Any) -> None:
        expected_type: Optional[str] = kwargs.get("expected_type")
        if expected_type is None and len(args) > 0:
            expected_type = args[0]

        expected_value: Optional[str] = kwargs.get("expected_value")
        if expected_value is None and len(args) > 1:
            expected_value = args[1]

        if not expected_type:
            raise ValueError(
                f"Test for source '{source}' did not provide an 'expected_type'."
            )

        tokens = list(moon_parser.lex(source))

        assert (
            len(tokens) == 1
        ), f"Expected exactly 1 token for '{source}', but got {len(tokens)}: {tokens}"

        actual_type = clean_type(tokens[0].type)
        assert (
            actual_type == expected_type
        ), f"Token type mismatch for '{source}'. Expected '{expected_type}', got '{actual_type}'"

        if expected_value is not None:
            assert (
                tokens[0].value == expected_value
                ), f"Token value mismatch for '{source}'. Expected '{expected_value}', got '{tokens[0].value}'"

        return func(moon_parser, source, *args, **kwargs)

    return wrapper


KEYWORDS = (
    (
        ("action", "ACTION"),
        ("and", "AND"),
        ("as", "AS"),
        # ("assert", "ASSERT"),     #🔒
        # ("async", "ASYNC"),       #🔒
        # ("await", "AWAIT"),       #🔒
        ("call", "CALL"),
        # ("continue", "CONTINUE"), #🔒
        # ("default", "DEFAULT"),   #🔒
        ("dict", "DICT"),
        ("elif", "ELIF"),
        ("else", "ELSE"),
        # ("end", "END"),           #🔒
        # ("error", "ERROR"),       #🔒
        ("false", "FALSE"),
        ("fail", "FAIL"),
        ("from", "FROM"),
        # ("for", "FOR"),           #🔒
        # ("global", "GLOBAL"),     #🔒
        ("has", "HAS"),
        ("if", "IF"),
        # ("in", "IN"),             #🔒
        ("is", "IS"),
        ("isnt", "ISNT"),
        # ("lambda", "LAMBDA"),     #🔒
        ("list", "LIST"),
        ("null", "NULL"),
        ("not", "NOT"),
        ("or", "OR"),
        # ("pass", "PASS"),         #🔒
        # ("raise", "RAISE"),       #🔒
        ("result", "RESULT"),
        ("test", "TEST"),
        ("thing", "THING"),
        ("true", "TRUE"),
        ("use", "USE"),
        ("skip", "SKIP"),
        ("stop", "STOP"),
        ("while", "WHILE"),
        # ("yield", "YIELD"),       #🔒
    )
)
@pytest.mark.parametrize("source, expected_type", [*KEYWORDS])
@assert_single_token
def test_lexer_keywords(moon_parser, source: str, expected_type: str) -> None: ...


OPERATORS = (
    ('+', "PLUS"),
    ('-', "MINUS"),
    ('*', "MULTIPLY"),
    ('/', "DIVIDE"),
    ("//", "FLOOR"),
    ("%", "MODULO"),
    ("**", "POWER"),
    ("<", "LT"),
    ("<=", "LTE"),
    (">", "GT"),
    (">=", "GTE"),
    ("is", "IS"),
    ("isnt", "ISNT"),
    ("not", "NOT"),
)
@pytest.mark.parametrize("source, expected_type", [*OPERATORS])
@assert_single_token
def test_lexer_operators(moon_parser: Lark, source: str, expected_type: str) -> None: ...


BOOLEAN_AND_NULL = (
    ("true", "TRUE"),
    ("false", "FALSE"),
    ("null", "NULL"),
)
@pytest.mark.parametrize("source, expected_type", [*BOOLEAN_AND_NULL])
@assert_single_token
def test_lexer_boolean_and_null(moon_parser: Lark, source: str, expected_type: str) -> None: ...


SIGNED_INTEGER = (
    '0',
    '1',
    "42",
    "4096",
    '-0',
    '-1',
    "-42",
    "-4096",
    '+0',
    '+1',
    "+42",
    "+4096",
)
@pytest.mark.parametrize("source, expected_type, expected_value", [(s, "SIGNED_INTEGER", s) for s in SIGNED_INTEGER])
@assert_single_token
def test_lexer_signed_integer(moon_parser: Lark, source: str, expected_type: str, expected_value: str) -> None: ...


SIGNED_FLOAT = (
    "0.0",
    "0.00000000",
    "1.1",
    ".0001",
    "1e10",
    "1E10",
    "1e-10",
    "1E-10",
    "1e+10",
    "1E+10",
    ".1e10",
    ".1E10",
    ".1e-10",
    ".1E-10",
    ".1e+10",
    ".1E+10",
    "-0.0",
    "-0.00000000",
    "-1.1",
    "-.0001",
    "-1e10",
    "-1E10",
    "-1e-10",
    "-1E-10",
    "-1e+10",
    "-1E+10",
    "-.1e10",
    "-.1E10",
    "-.1e-10",
    "-.1E-10",
    "-.1e+10",
    "-.1E+10",
    "+0.0",
    "+0.00000000",
    "+1.1",
    "+.0001",
    "+1e10",
    "+1E10",
    "+1e-10",
    "+1E-10",
    "+1e+10",
    "+1E+10",
    "+.1e10",
    "+.1E10",
    "+.1e-10",
    "+.1E-10",
    "+.1e+10",
    "+.1E+10",
)
@pytest.mark.parametrize("source, expected_type, expected_value", [(s, "SIGNED_FLOAT", s) for s in SIGNED_FLOAT])
@assert_single_token
def test_lexer_signed_float(moon_parser: Lark, source: str, expected_type: str, expected_value: str) -> None: ...


ESCAPED_STRING = (
    '"string"',
    "'string'",
    "'string\\\\'",
    "''",
    '""',
    '"string with spaces"',
    "'string with spaces'",
    '"string with (parens) {} []"',
    "'string with (parens) {} []'",
    '"string with \\"quotes\\""',
    "'string with \\'quotes\\''",
    '"string with \\\\ backslash"',
    "'string with \\\\ backslash'",
    '"string with \\n new line"',
    "'string with \\n new line'",
    '"string with \\t tabulation"',
    "'string with \\t tabulation'",
    '"string with \\u2600 unicode"',
    "'string with \\u2600 unicode'",
    '"emoji 🍎"',
    "'emoji 🍎'",
)
@pytest.mark.parametrize("source, expected_type, expected_value", [(s, "ESCAPED_STRING", s) for s in ESCAPED_STRING])
@assert_single_token
def test_lexer_escaped_string(moon_parser: Lark, source: str, expected_type: str, expected_value: str) -> None: ...


IDENTIFIER = (
    "🍎",
    "apple",
    "display_name",
    "Data_1",
    "x",
    "X",
    "__private",
    "A1234567890",
    "__init__",
    "a_",
    "a_" * 50,
    '🧠',
    "truefalse",
    "null0",
    "action1",
)
@pytest.mark.parametrize("source, expected_type, expected_value", [(s, "IDENTIFIER", s) for s in IDENTIFIER])
@assert_single_token
def test_lexer_identifier(moon_parser: Lark, source: str, expected_type: str, expected_value: str) -> None: ...


@pytest.mark.parametrize("invalid_token", [
    '$',
    '@',
    '&',
    '^',
    '~',
    '`',
])
def test_invalid_tokens(moon_parser: Lark, invalid_token):
    with pytest.raises(UnexpectedCharacters):
        list(moon_parser.lex(invalid_token))