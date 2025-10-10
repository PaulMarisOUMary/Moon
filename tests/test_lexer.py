import pytest
from typing import Tuple

from lark.exceptions import UnexpectedCharacters

KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("action", "ACTION"),
    ("and", "AND"),
    ("as", "AS"),
    # ("assert", "ASSERT"),     🔒
    # ("async", "ASYNC"),       🔒
    # ("await", "AWAIT"),       🔒
    # ("call", "CALL"),🚧
    # ("continue", "CONTINUE"), 🔒
    # ("default", "DEFAULT"),   🔒
    # ("dict", "DICT"),🚧
    # ("elif", "ELIF"),         🔒 
    ("else", "ELSE"),
    # ("end", "END"),           🔒
    # ("error", "ERROR"),       🔒
    ("false", "FALSE"),
    ("fail", "FAIL"),
    ("from", "FROM"),
    # ("for", "FOR"),           🔒
    # ("global", "GLOBAL"),     🔒
    ("has", "HAS"),
    ("if", "IF"),
    # ("in", "IN"),             🔒
    ("is", "IS"),
    # ("isnt", "ISNT"), 🗑️
    # ("lambda", "LAMBDA"),     🔒
    # ("list", "LIST"),🚧
    ("null", "NULL"),
    ("not", "NOT"),
    ("or", "OR"),
    # ("pass", "PASS"),         🔒
    # ("raise", "RAISE"),       🔒
    ("result", "RESULT"),
    ("test", "TEST"),
    ("thing", "THING"),
    ("true", "TRUE"),
    ("use", "USE"),
    ("skip", "SKIP"),
    ("stop", "STOP"),
    ("while", "WHILE"),
    # ("yield", "YIELD"),       🔒
)

# Test tokens
@pytest.mark.parametrize("source, expected_t_type", [
    *KEYWORDS,
])
def test_t_tokens(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test operators
@pytest.mark.parametrize("source, expected_t_type", [
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
    # ("isnt", "ISNT"),
    ("not", "NOT"),
])
def test_t_operators(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid newline
@pytest.mark.parametrize("source, expected_n_type", [
    ('\n', 1),
    ("\r\n", 1),
    ("\n\n", 1),
    ("thing\nthing\n", 2),
    ("thing\r\nthing\r\n", 2),
    ("thing\n\nthing\n", 2),
    ("thing\r\n\r\nthing\r\n", 2),
    ("thing\n    thing\n", 2),
])
def test_t_newline(parser, source, expected_n_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    n_t_newline = [t for t in tokens if t.type == "_NEWLINE"]
    assert len(n_t_newline) == expected_n_type

# Test comments are ignored
@pytest.mark.parametrize("source", [
    "# this is a (single line comment)\n",
    "( this is a multi-line\n comment \n \n \n\n ((: )\n",
    "(\n\n\n\n this is a multi-line comment \n \n \n\n ((: )\n",
])
def test_t_comment(parser, source):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == "_NEWLINE"

# Test whitespace are ignored
@pytest.mark.parametrize("source", [
    ' ',
    '\t',
    '\f',
    "thing   ",
    "thing\tthing",
])
def test_t_whitespace(parser, source):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert all(t.type != "WS" for t in tokens)

# Test valid boolean
@pytest.mark.parametrize("source, expected_t_type", [
    ("true", "TRUE"),
    ("false", "FALSE"),
])
def test_t_boolean(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid null
@pytest.mark.parametrize("source, expected_t_type", [
    ("null", "NULL"),
])
def test_t_null(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid signed integer
SIGNED_INTEGER_CASES = [
    '0',
    "1",
    "4096",
    "-1",
    "-4096",
    "+1",
    "+4096",
]
@pytest.mark.parametrize("source, expected_t_type", [(s, "SIGNED_INTEGER") for s in SIGNED_INTEGER_CASES])
def test_t_integer(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid signed float
SIGNED_FLOAT_CASES = [
    "1.1",
    "0.00000000",
    ".0001",
    "-1.1",
    "-0.00000000",
    "-0.0001",
    "-.0001",
    "+1.1",
    "+0.00000000",
    "+0.0001",
    "+.0001",
    "1e10",
    "1E10",
    "-1e-10",
    "+.5e+2"
]
@pytest.mark.parametrize("source, expected_t_type", [(s, "SIGNED_FLOAT") for s in SIGNED_FLOAT_CASES])
def test_t_float(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid escaped string
ESCAPED_STRING_CASES = [
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
]
@pytest.mark.parametrize("source, expected_t_type", [(s, "ESCAPED_STRING") for s in ESCAPED_STRING_CASES])
def test_t_string(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test valid identifier
IDENTIFIER_CASES = [
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
]
@pytest.mark.parametrize("source, expected_t_type", [(i, "IDENTIFIER") for i in IDENTIFIER_CASES])
def test_t_identifier(parser, source, expected_t_type):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == expected_t_type

# Test invalid identifiers named as keywords
@pytest.mark.parametrize("invalid_identifier", [
    *[k[0] for k in KEYWORDS],
])
def test_invalid_identifier_named_as_keyword(parser, invalid_identifier):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(invalid_identifier))

    # Assert
    assert len(tokens) == 1
    assert tokens[0].type != "IDENTIFIER"

# Test valid indent/dedent
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
def test_t_tabulation(parser, source, expected_n_indent, expected_n_dedent):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    n_t_indent = [t for t in tokens if t.type == "_INDENT"]
    n_t_dedent = [t for t in tokens if t.type == "_DEDENT"]

    assert len(n_t_indent) == expected_n_indent
    assert len(n_t_dedent) == expected_n_dedent

# Test invalid tokens
@pytest.mark.parametrize("invalid_token", [
    '$',
    '@',
    '&',
    '^',
    '~',
    '`',
])
def test_invalid_tokens(parser, invalid_token):
    # Arrange
    lark = parser

    # Act & Assert
    with pytest.raises(UnexpectedCharacters):
        list(lark.lex(invalid_token))

# Test invalid identifiers
@pytest.mark.parametrize("invalid_identifier", [
    "!error",
    "@hello",
    "hello@",
    "hello.world",
])
def test_invalid_identifier(parser, invalid_identifier):
    # Arrange
    lark = parser

    # Act & Assert
    with pytest.raises(UnexpectedCharacters):
        list(lark.lex(invalid_identifier))

# Test valid and invalid boolean literals
@pytest.mark.parametrize("source, is_valid", [
    ("true", True),
    ("false", True),
    ("True", False),
    ("False", False),
    ("tru", False),
    ("fals", False),
])
def test_valid_and_invalid_boolean(parser, source, is_valid):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert tokens[0].type in ("TRUE", "FALSE") if is_valid else "IDENTIFIER"

# Test valid and invalid null literal
@pytest.mark.parametrize("source, is_valid", [
    ("null", True),
    ("nul", False),
    ("Null", False),
    ("nulL", False),
    ("NULL", False),
])
def test_valid_and_invalid_null(parser, source, is_valid):
    # Arrange
    lark = parser

    # Act
    tokens = list(lark.lex(source))

    # Assert
    assert tokens[0].type == "NULL" if is_valid else "IDENTIFIER"

# Test line numbers
@pytest.mark.parametrize("source, expected_line_number", [
    ("""""", 0),
    ("""1
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
    ("""
""", 1),
    ("""









expression
""", 11)
    ]
)
def test_line_numbers(parser, source, expected_line_number):
    # Arrange
    lexer = parser

    # Act
    tokens = list(lexer.lex(source))

    # Assert
    if tokens:
        assert tokens[-1].line == expected_line_number
    else:
        assert expected_line_number == 0