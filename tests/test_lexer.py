import pytest

from functools import wraps
from typing import Any, Callable, Optional

from lark import Lark
from lark.exceptions import UnexpectedCharacters

from .utils import clean_type


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
        ("raise", "RAISE"),
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
def test_lexer_keywords(moon_parser: Lark, source: str, expected_type: str) -> None: ...


AMBIGUOUS_TERMS = (
    ('.', "DOT"),
    ("...", "ELLIPSIS"),
    ('/', "DIVIDE"),
    ("//", "FLOOR"),
    ('<', "LT"),
    ("<=", "LTE"),
    ('>', "GT"),
    (">=", "GTE"),
    ("is", "IS"),
    ("isnt", "ISNT"),
)
@pytest.mark.parametrize("source, expected_type", [*AMBIGUOUS_TERMS])
@assert_single_token
def test_lexer_ambiguous_terms(moon_parser: Lark, source: str, expected_type: str) -> None: ...


OPERATORS = (
    ('+', "PLUS"),
    ('-', "MINUS"),
    ('*', "MULTIPLY"),
    ('/', "DIVIDE"),
    ("//", "FLOOR"),
    ("%", "MODULO"),
    ("**", "POWER"),
    ('<', "LT"),
    ("<=", "LTE"),
    ('>', "GT"),
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
    '🍎',
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


@pytest.mark.parametrize("source, n_expected", [
    ('\n', 1),
    ("\r\n", 1),
    ("\n\n", 1),
    ("thing\nthing\n", 2),
    ("thing\r\nthing\r\n", 2),
    ("thing\n\nthing\n", 2),
    ("thing\r\n\r\nthing\r\n", 2),
    ("thing\n    thing\n", 2),
])
def test_lexer_newline(moon_parser: Lark, source: str, n_expected: int) -> None:
    tokens = list(moon_parser.lex(source))

    n_newline = [t for t in tokens if clean_type(t.type) == "_NEWLINE"]
    assert len(n_newline) == n_expected


@pytest.mark.parametrize("source, expected_n_indent, expected_n_dedent", [
    ('\t', 0, 0),
    ("\t\t", 0, 0),
    ("thing\n\t0", 1, 1),
    ("thing\n    a", 1, 1),
    ("thing\n\tthing\n\t\ta", 2, 2),
    ("thing\n    thing\n        a", 2, 2),
    ("""to_guess is 14

# Version using while, skip and stop

while true
    guess is ask "Type your guess: "

    if guess isnt to_guess
        if guess < to_guess
            print "Its More"
        else
            print "Its Less"
        skip

    stop

print 'Congrats you won !'""", 4, 4),
    ("""var is 14
while true
    guess is ask "Type your guess: "

    if guess isnt var
        if guess > 1
            if guess > 2
                if guess > 3
                    if guess > 4
                        print "Its More (:"
        skip
    stop

print 'Congrats you won !'""", 6, 6),
])
def test_lexer_tabulation(moon_parser: Lark, source: str, expected_n_indent: int, expected_n_dedent: int) -> None:
    tokens = list(moon_parser.lex(source))

    n_indent = [t for t in tokens if clean_type(t.type) == "_INDENT"]
    n_dedent = [t for t in tokens if clean_type(t.type) == "_DEDENT"]

    assert len(n_indent) == expected_n_indent
    assert len(n_dedent) == expected_n_dedent


@pytest.mark.parametrize("source", [
    '$',
    '@',
    '&',
    '=',
    '}',
    '{',
    '[',
    ']',
    '^',
    '~',
    '`',
])
def test_lexer_invalid_tokens(moon_parser: Lark, source: str) -> None:
    with pytest.raises(UnexpectedCharacters):
        list(moon_parser.lex(source))


@pytest.mark.parametrize("source", [
    ' ',
    '\t',
    '\f',
    "thing   ",
    "thing\tthing",
])
def test_lexer_ignored_whitespace(moon_parser: Lark, source: str) -> None:
    tokens = list(moon_parser.lex(source))

    assert all(t.type != "WS" for t in tokens)


@pytest.mark.parametrize("source", [
    "# this is a (single line comment)\n",
    "( this is a multi-line\n comment \n \n \n\n ((: )\n",
    "(\n\n\n\n this is a multi-line comment \n \n \n\n ((: )\n",
])
def test_lexer_ignored_comment(moon_parser: Lark, source: str) -> None:
    tokens = list(moon_parser.lex(source))

    assert len(tokens) == 1
    assert tokens[0].type == "_NEWLINE"


INVALID_IDENTIFIER = (
    "1apple",
    "100_000",
    "🍎apple",
    "apple🍎",
    "w🐋e",
    "10_",
    # "_",
)
@pytest.mark.parametrize("source", [*INVALID_IDENTIFIER])
def test_lexer_invalid_identifier(moon_parser: Lark, source: str) -> None:
    try:
        tokens = list(moon_parser.lex(source))

        if len(tokens) == 1:
            assert clean_type(tokens[0].type) != "IDENTIFIER"
    except UnexpectedCharacters:
        pass


@pytest.mark.parametrize("source, expected_line", [
    (r'', 0),
    (r"""1
2
3
4
5
6
7
8
9
10
11
""", 11),
    (r"""
""", 1),
    (r"""









expression
""", 11)
    ]
)
def test_line_numbers(moon_parser: Lark, source: str, expected_line: int) -> None:
    tokens = list(moon_parser.lex(source))

    if tokens:
        assert tokens[-1].line == expected_line
    else:
        assert expected_line == 0