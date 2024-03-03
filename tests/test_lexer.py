import pytest

from moon import build_lexer

# Test valid boolean
@pytest.mark.parametrize("valid_boolean", [
	"true",
	"false",
])
def test_t_boolean(valid_boolean):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_boolean)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "BOOLEAN"
	assert len(lexer.errors) == 0

# Test valid identifier
@pytest.mark.parametrize("valid_identifier", [
	"🍎",
	"apple",
	"display_name",
	"Data_1",
	"x",
	"X",
	"__private",
])
def test_t_identifier(valid_identifier):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_identifier)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "IDENTIFIER"
	assert len(lexer.errors) == 0

# Test valid float
@pytest.mark.parametrize("valid_float", [
	"1.1",
	"0.00000000",
])
def test_t_float(valid_float):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_float)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "FLOAT"
	assert len(lexer.errors) == 0

# Test valid integer
@pytest.mark.parametrize("valid_integer", [
	"0",
	"1",
	"4096",
])
def test_t_integer(valid_integer):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_integer)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "INTEGER"
	assert len(lexer.errors) == 0

# Test valid string
@pytest.mark.parametrize("valid_string", [
	'"string"',
	"'string'",
	"'string\\\\'",
	"''",
	'""',
])
def test_t_string(valid_string):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_string)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "STRING"
	assert len(lexer.errors) == 0

# Test valid comment
@pytest.mark.parametrize("valid_comment", [
	"# this is a (single line comment)",
])
def test_t_comment(valid_comment):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_comment)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 0
	assert len(lexer.errors) == 0

# Test valid multiline_comment
@pytest.mark.parametrize("valid_multiline_comment", [
	"( this is a multi-line\n comment \n \n \n\n ((: )",
])
def test_t_multiline_comment(valid_multiline_comment):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_multiline_comment)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 0
	assert len(lexer.errors) == 0

# Test valid tabulation
@pytest.mark.parametrize("valid_tabulation", [
	"\t",
])
def test_t_tabulation(valid_tabulation):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_tabulation)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "TABULATION"
	assert len(lexer.errors) == 0

# Test valid newline
@pytest.mark.parametrize("valid_newline", [
	"a\nb",
])
def test_t_newline(valid_newline):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_newline)
	tokens = list(lexer)

	# Assert
	assert tokens[1].type == "NEWLINE"
	assert len(lexer.errors) == 0

# Test valid plus
@pytest.mark.parametrize("valid_plus", [
	"+",
])
def test_t_plus(valid_plus):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_plus)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "PLUS"
	assert len(lexer.errors) == 0

# Test valid minus
@pytest.mark.parametrize("valid_minus", [
	"-",
])
def test_t_minus(valid_minus):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_minus)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "MINUS"
	assert len(lexer.errors) == 0

# Test valid multiply
@pytest.mark.parametrize("valid_multiply", [
	"*",
])
def test_t_multiply(valid_multiply):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_multiply)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "MULTIPLY"
	assert len(lexer.errors) == 0

# Test valid divide
@pytest.mark.parametrize("valid_divide", [
	"/",
])
def test_t_divide(valid_divide):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_divide)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "DIVIDE"
	assert len(lexer.errors) == 0

# Test valid modulo
@pytest.mark.parametrize("valid_modulo", [
	"%",
])
def test_t_modulo(valid_modulo):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_modulo)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "MODULO"
	assert len(lexer.errors) == 0

# Test valid exponent
@pytest.mark.parametrize("valid_exponent", [
	"**",
])
def test_t_exponent(valid_exponent):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_exponent)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "EXPONENT"
	assert len(lexer.errors) == 0

# Test valid lt
@pytest.mark.parametrize("valid_lt", [
	"<",
])
def test_t_lt(valid_lt):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_lt)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "LT"
	assert len(lexer.errors) == 0

# Test valid le
@pytest.mark.parametrize("valid_le", [
	"<=",
])
def test_t_le(valid_le):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_le)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "LE"
	assert len(lexer.errors) == 0

# Test valid gt
@pytest.mark.parametrize("valid_gt", [
	">",
])
def test_t_gt(valid_gt):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_gt)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "GT"
	assert len(lexer.errors) == 0

# Test valid ge
@pytest.mark.parametrize("valid_ge", [
	">=",
])
def test_t_ge(valid_ge):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_ge)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "GE"
	assert len(lexer.errors) == 0

# Test valid action
@pytest.mark.parametrize("valid_action", [
	"action",
])
def test_t_action(valid_action):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_action)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "ACTION"
	assert len(lexer.errors) == 0

# Test valid and
@pytest.mark.parametrize("valid_and", [
	"and",
])
def test_t_and(valid_and):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_and)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "AND"
	assert len(lexer.errors) == 0

# Test valid as
@pytest.mark.parametrize("valid_as", [
	"as",
])
def test_t_as(valid_as):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_as)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "AS"
	assert len(lexer.errors) == 0

# Test valid ask
@pytest.mark.parametrize("valid_ask", [
	"ask",
])
def test_t_ask(valid_ask):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_ask)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "ASK"
	assert len(lexer.errors) == 0

# Test valid call
@pytest.mark.parametrize("valid_call", [
	"call",
])
def test_t_call(valid_call):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_call)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "CALL"
	assert len(lexer.errors) == 0

# Test valid dict
@pytest.mark.parametrize("valid_dict", [
	"dict",
])
def test_t_dict(valid_dict):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_dict)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "DICT"
	assert len(lexer.errors) == 0

# Test valid else
@pytest.mark.parametrize("valid_else", [
	"else",
])
def test_t_else(valid_else):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_else)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "ELSE"
	assert len(lexer.errors) == 0

# Test valid fail
@pytest.mark.parametrize("valid_fail", [
	"fail",
])
def test_t_fail(valid_fail):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_fail)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "FAIL"
	assert len(lexer.errors) == 0

# Test valid from
@pytest.mark.parametrize("valid_from", [
	"from",
])
def test_t_from(valid_from):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_from)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "FROM"
	assert len(lexer.errors) == 0

# Test valid has
@pytest.mark.parametrize("valid_has", [
	"has",
])
def test_t_has(valid_has):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_has)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "HAS"
	assert len(lexer.errors) == 0

# Test valid if
@pytest.mark.parametrize("valid_if", [
	"if",
])
def test_t_if(valid_if):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_if)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "IF"
	assert len(lexer.errors) == 0

# Test valid is
@pytest.mark.parametrize("valid_is", [
	"is",
])
def test_t_is(valid_is):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_is)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "IS"
	assert len(lexer.errors) == 0

# Test valid isnt
@pytest.mark.parametrize("valid_isnt", [
	"isnt",
])
def test_t_isnt(valid_isnt):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_isnt)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "ISNT"
	assert len(lexer.errors) == 0

# Test valid list
@pytest.mark.parametrize("valid_list", [
	"list",
])
def test_t_list(valid_list):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_list)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "LIST"
	assert len(lexer.errors) == 0

# Test valid null
@pytest.mark.parametrize("valid_null", [
	"null",
])
def test_t_null(valid_null):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_null)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "NULL"
	assert len(lexer.errors) == 0

# Test valid not
@pytest.mark.parametrize("valid_not", [
	"not",
])
def test_t_not(valid_not):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_not)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "NOT"
	assert len(lexer.errors) == 0

# Test valid or
@pytest.mark.parametrize("valid_or", [
	"or",
])
def test_t_or(valid_or):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_or)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "OR"
	assert len(lexer.errors) == 0

# Test valid print
@pytest.mark.parametrize("valid_print", [
	"print",
])
def test_t_print(valid_print):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_print)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "PRINT"
	assert len(lexer.errors) == 0

# Test valid raise
@pytest.mark.parametrize("valid_raise", [
	"raise",
])
def test_t_raise(valid_raise):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_raise)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "RAISE"
	assert len(lexer.errors) == 0

# Test valid result
@pytest.mark.parametrize("valid_result", [
	"result",
])
def test_t_result(valid_result):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_result)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "RESULT"
	assert len(lexer.errors) == 0

# Test valid test
@pytest.mark.parametrize("valid_test", [
	"test",
])
def test_t_test(valid_test):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_test)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "TEST"
	assert len(lexer.errors) == 0

# Test valid thing
@pytest.mark.parametrize("valid_thing", [
	"thing",
])
def test_t_thing(valid_thing):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_thing)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "THING"
	assert len(lexer.errors) == 0

# Test valid use
@pytest.mark.parametrize("valid_use", [
	"use",
])
def test_t_use(valid_use):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_use)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "USE"
	assert len(lexer.errors) == 0

# Test valid skip
@pytest.mark.parametrize("valid_skip", [
	"skip",
])
def test_t_skip(valid_skip):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_skip)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "SKIP"
	assert len(lexer.errors) == 0

# Test valid stop
@pytest.mark.parametrize("valid_stop", [
	"stop",
])
def test_t_stop(valid_stop):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_stop)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "STOP"
	assert len(lexer.errors) == 0



# Test indent
@pytest.mark.parametrize("input_str, n_indent", [
	('', 0),
	('\t', 0),
	('l1\n\tl2', 1),
	('l1\n\tl2\n\t\tl3', 2),
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

print 'Congrats you won !'""", 4),
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

print 'Congrats you won !'""", 6),
])
def test_t_indent(input_str, n_indent):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	n_t_indent = [token for token in tokens if token.type == "INDENT"]

	assert len(n_t_indent) == n_indent
	assert len(lexer.errors) == 0

# Test dedent
@pytest.mark.parametrize("input_str, n_dedent", [
	('', 0),
	('\t', 0),
	('l1\n\tl2', 1),
	('l1\n\tl2\n\t\tl3', 2),
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

print 'Congrats you won !'""", 4),
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

print 'Congrats you won !'""", 6),
])
def test_t_dedent(input_str, n_dedent):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(input_str)
	tokens = list(lexer)

	# Assert
	n_t_dedent = [token for token in tokens if token.type == "DEDENT"]

	print(n_t_dedent)

	assert len(n_t_dedent) == n_dedent
	assert len(lexer.errors) == 0



# Test indent
@pytest.mark.parametrize("valid_while", [
	"while",
])
def test_t_while(valid_while):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(valid_while)
	tokens = list(lexer)

	# Assert
	assert len(tokens) == 1
	assert tokens[0].type == "WHILE"
	assert len(lexer.errors) == 0



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
    ("continue", "CONTINUE", '❌'),
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
    ("skip",     "SKIP",     '✅'),
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

# Test invalid identifiers
@pytest.mark.parametrize("invalid_identifier", [
	"🍎🍎",
	"display-name",
	"11Data",
])
def test_invalid_identifier(invalid_identifier):
	# Arrange
	lexer = build_lexer()

	# Act
	lexer.input(invalid_identifier)
	tokens = list(lexer)

	# Assert
	assert len(tokens) != 1 or len(lexer.errors) > 0

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
	("'string here'", True),
	("'string with \\'escape\\' characters'", True),
	("'string with \\n new line'", True),
	("'unterminated string", False),
	("'string with unmatched \\'", False),
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