import pytest

from moon import build_lexer

# Test valid tokens
@pytest.mark.parametrize("input_str, expected_type, is_detected", [
    ("+",        "PLUS",     '✅'),
    ("-",        "MINUS",    '✅'),
    ("*",        "MULTIPLY", '✅'),
    ("/",        "DIVIDE",   '✅'),
    ("%",        "MODULO",   '✅'),
    ("**",       "EXPONENT", '✅'),
    ("<",        "LT",       '✅'),
    ("<=",       "LE",       '✅'),
    (">",        "GT",       '✅'),
    (">=",       "GE",       '✅'),
    ("action",   "ACTION",   '✅'),
    ("and",      "AND",      '✅'),
    ("as",       "AS",       '✅'),
    ("ask",      "ASK",      '✅'),
    ("assert",   "ASSERT",   '❌'),
    ("async",    "ASYNC",    '❌'),
    ("await",    "AWAIT",    '❌'),
    ("call",     "CALL",     '✅'),
    ("continue", "CONTINUE", '✅'),
    ("default",  "DEFAULT",  '❌'),
    ("dict",     "DICT",     '✅'),
    ("elif",     "ELIF",     '❌'),
    ("else",     "ELSE",     '✅'),
    ("end",      "END",      '❌'),
    ("false",    "BOOLEAN",  '✅'),
    ("fail",     "FAIL",     '✅'),
    ("from",     "FROM",     '✅'),
    ("for",      "FOR",      '❌'),
    ("global",   "GLOBAL",   '❌'),
    ("has",      "HAS",      '✅'),
    ("if",       "IF",       '✅'),
    ("in",       "IN",       '❌'),
    ("is",       "IS",       '✅'),
    ("isnt",     "ISNT",     '✅'),
    ("lambda",   "LAMBDA",   '❌'),
    ("list",     "LIST",     '✅'),
    ("null",     "NULL",     '✅'),
    ("not",      "NOT",      '✅'),
    ("nothing",  "NOTHING",  '❌'),
    ("or",       "OR",       '✅'),
    ("pass",     "PASS",     '❌'),
    ("print",    "PRINT",    '✅'),
    ("raise",    "RAISE",    '✅'),
    ("result",   "RESULT",   '✅'),
    ("test",     "TEST",     '✅'),
    ("thing",    "THING",    '✅'),
    ("true",     "BOOLEAN",  '✅'),
    ("use",      "USE",      '✅'),
    ("stop",     "STOP",     '✅'),
    ("while",    "WHILE",    '✅'),
    ("yield",    "YIELD",    '❌'),
])
def test_valid_tokens(input_str, expected_type, is_detected):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	if is_detected == '✅':
		assert tokens[0].type == expected_type
		assert len(lexer.errors) == 0
	else:
		assert len(tokens) == 1
		assert tokens[0].type != expected_type
		assert tokens[0].type == "IDENTIFIER"
		assert len(lexer.errors) == 0

# Test invalid identifiers named as keywords
@pytest.mark.parametrize("invalid_identifier", [
	"true",
	"false",
	"null",
	"0.0",
	"-",
	'"jaaj"',
	"action",
	"result",
	"thing",
])
def test_invalid_identifier_named_as_keyword(invalid_identifier):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(invalid_identifier)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type != "IDENTIFIER"
	assert len(lexer.errors) == 0

# Test invalid tokens
@pytest.mark.parametrize("invalid_token", [
	"$",
	"@",
	"&",
	"^",
	"~",
	"`",
])
def test_invalid_tokens(invalid_token):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(invalid_token)
	tokens = list(lexer)

	# Assert
	assert lexer.errors[0][0] == invalid_token

# Test valid and invalid boolean literals
@pytest.mark.parametrize("input_str, is_valid", [
	("true", True),
	("false", True),
	("True", False),  # Case-sensitive
	("False", False),  # Case-sensitive
	("tru", False),
	("fals", False),
])
def test_valid_and_invalid_boolean(input_str, is_valid):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	assert tokens[0].type == "BOOLEAN" if is_valid else "IDENTIFIER"

# Test valid and invalid null literal
@pytest.mark.parametrize("input_str, is_valid", [
	("null", True),
	("nul", False),
	("Null", False),
	("nulL", False),
	("NULL", False),
])
def test_valid_and_invalid_null(input_str, is_valid):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	assert tokens[0].type == "NULL" if is_valid else "IDENTIFIER"

# Test valid and invalid string literals
@pytest.mark.parametrize("input_str, is_valid", [
	('"string here"', True),
	('"string with \\"escape\\" characters"', True),
	('"string with \\n new line"', True),
	('"unterminated string', False),
	('"string with unmatched \\"', False),
])
def test_valid_and_invalid_string(input_str, is_valid):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	assert tokens[0].type == "STRING" if is_valid else "IDENTIFIER"
	assert len(tokens) == 1 if is_valid else len(tokens) > 1

# Test valid and invalid integer literals
@pytest.mark.parametrize("input_str, expected_type, is_valid", [
	("0", "INTEGER", True),
	("1", "INTEGER", True),
	("123", "INTEGER", True),
	("1234567890", "INTEGER", True),
	("01", "INTEGER", False),
	("0123", "INTEGER", False),
	("1.", "INTEGER", False),
	(".123", "INTEGER", False),
])
def test_valid_and_invalid_integer(input_str, expected_type, is_valid):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	if is_valid:
		assert tokens[0].type == expected_type
	else:
		assert len(lexer.errors) > 0

# Test valid and invalid floating-point literals
@pytest.mark.parametrize("input_str, expected_type, is_valid", [
	("0.0", "FLOAT", True),
	("1.0", "FLOAT", True),
	("123.456", "FLOAT", True),
	("1234567890.1234567890", "FLOAT", True),
	("0.", "FLOAT", False),
	("0.123", "FLOAT", True),
	("123.", "FLOAT", False),
	("12.34.56", "FLOAT", False),
	(".456", "FLOAT", False),
])
def test_valid_and_invalid_float(input_str, expected_type, is_valid):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	if is_valid:
		assert tokens[0].type == expected_type
	else:
		assert len(lexer.errors) > 0

# Test line numbers
@pytest.mark.parametrize("input_str, expected_line_number", [
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
def test_line_numbers(input_str, expected_line_number):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	if len(tokens) > 0:
		assert tokens[-1].lineno == expected_line_number
	else:
		assert len(lexer.errors) == 0