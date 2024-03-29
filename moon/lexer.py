import ply.lex as lex

from typing import Any

reserved_keywords = [
	("action",   "ACTION",   '✅'),
	("and",      "AND",      '✅'),
	("as",       "AS",       '✅'),
	("ask",      "ASK",      '✅'),
	("assert",   "ASSERT",   '❌'),
	("async",    "ASYNC",    '❌'),
	("await",    "AWAIT",    '❌'),
	("call",     "CALL",     '✅'),
	("default",  "DEFAULT",  '❌'),
	("dict",     "DICT",     '✅'),
	("elif",     "ELIF",     '❌'),
	("else",     "ELSE",     '✅'),
	("end",      "END",      '❌'),
	#("false",    "BOOLEAN",  '✅'),
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
	#("true",     "BOOLEAN",  '✅'),
	("use",      "USE",      '✅'),
	("skip",     "SKIP",     '✅'),
	("stop",     "STOP",     '✅'),
	("while",    "WHILE",    '✅'),
	("yield",    "YIELD",    '❌'),
]

# A string containing ignored characters (spaces and tabs)
t_ignore = ' '

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r"-(?!\d+)"
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EXPONENT = r"\*\*"
t_LT = r'<'
t_LE = r"<="
t_GT = r'>'
t_GE = r">="

# Reserved words
reserved = {
	k: v 
	for k, v, used in reserved_keywords 
	if used == '✅'
}

# List of token names
tokens = [
	"INDENT", "DEDENT",
	"TABULATION", "NEWLINE",
	"COMMENT", "MULTILINE_COMMENT",
	"IDENTIFIER", "INTEGER", "FLOAT", "STRING", "BOOLEAN",
	"PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO", "EXPONENT",
	"LT", "LE", "GT", "GE", #"EQ", "NE",
] + list(reserved.values())

# Boolean literal rule
def t_BOOLEAN(t):
	r"\b(true|false)"
	t.value = (t.value == "true")
	return t

# Identifier rule
def t_IDENTIFIER(t):
	r"[a-zA-Z_][a-zA-Z_0-9]*|[\U0000231A-\U0001FAF8]"
	t.type = reserved.get(t.value, "IDENTIFIER")  # Check for reserved words
	# Might raise a warning if reserved (but not used) keyword detected
	return t

# Floating-point literal rule
def t_FLOAT(t):
	r"[+-]?(?!0[0-9])[0-9]*[.][0-9]*\b"
	t.value = float(t.value)
	return t

# Integer literal rule
def t_INTEGER(t):
	r"[+-]?(?!0[0-9])[0-9]+\b"
	t.value = int(t.value)
	return t

# String literal rule
def t_STRING(t):
	r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''
	t.value = t.value[1:-1]  # Remove the quotes
	return t

# Comment rule for single-line comments
def t_COMMENT(t):
	r"\#[^\n]*(\n)*"
	t.lexer.lineno += t.value.count('\n')
	# No return value. Token discarded

# Comment rule for multi-line comments
def t_MULTILINE_COMMENT(t):
	r"\([\s\S]*?\)"
	t.lexer.lineno += t.value.count('\n')
	# No return value. Token discarded

# Tabulation rule
def t_TABULATION(t):
	r'\t'
	return t

# Newline rule
def t_NEWLINE(t):
	r"\n+"
	t.lexer.lineno += t.value.count("\n")
	return t

# Error handling
def t_error(t):
	print(f"Error: '{str(t.value).strip()}' at line {t.lineno}:{t.lexpos}")
	t.lexer.errors.append([t.value[0], t.lexer.lineno, t.lexer.lexpos])
	t.lexer.skip(1)

# ===== Lexer handling =====

class LexTokenT(lex.LexToken):
	value: Any
	lineno: int
	lexpos: int
	type: str

	def __init__(self, value: Any, lineno: int, lexpos: int, type: str) -> None:
		self.value = value
		self.lineno = lineno
		self.lexpos = lexpos # lexpos == 0 for (INDENT || DEDENT)
		self.type = type

class IndentLexer():
	def __init__(self, **kwargs) -> None:
		self.lexer: lex.Lexer = lex.lex(**kwargs)
		self.lexer.errors = [] # type: ignore
		self.token_stream = None

	@property
	def errors(self):
		"""This array holds a list of errors encountered (e.g., syntax errors).
		It is populated after iterating through the input data using the lexer."""
		return self.lexer.errors # type: ignore

	def _indentation_filter(self, tokens):
		current_indentation = 0
		indentation_count = 0
		is_first_token = True
		token = None

		for token in tokens:
			if token.type == "NEWLINE":
				if is_first_token:  # Skip the first newline
					continue

				indentation_count = 0

				yield token

				next_token = next(tokens, None)
				while next_token and next_token.type == "TABULATION":
					indentation_count += 1
					next_token = next(tokens, None)

				if indentation_count > current_indentation:
					yield LexTokenT(
						value=indentation_count * '\t',
						lineno=token.lineno,
						lexpos=0,
						type="INDENT",
					)

				if indentation_count < current_indentation:
					for i in range(current_indentation - indentation_count):
						yield LexTokenT(
							value=(current_indentation-(i+1))*'\t',
							lineno=token.lineno,
							lexpos=0,
							type="DEDENT",
						)

				current_indentation = indentation_count

				if next_token:
					yield next_token
			else:
				yield token

			is_first_token = False

		for i in range(current_indentation):
			yield LexTokenT(
				value=(current_indentation-i)*'\t',
				lineno=token.lineno if token else 0,
				lexpos=0,
				type="DEDENT",
			)

	def _indent_tokens(self, lexer: lex.Lexer):
		tokens = iter(lexer.token, None)
		for token in self._indentation_filter(tokens):
			yield token

	def input(self, data):
		self.lexer.input(data)
		self.token_stream = self._indent_tokens(self.lexer)

	def __iter__(self):
		if self.token_stream is None:
			raise ValueError("The token_stream attribute is None, did you use input() ?")

		return iter(self.token_stream)

	def token(self):
		if self.token_stream is None:
			raise ValueError("The token_stream attribute is None, did you use input() ?")

		try:
			return next(self.token_stream)
		except StopIteration:
			return None

def print_tokens(code: str):
	lexer = build_lexer()
	lexer.input(code)

	for token in lexer:
		print(token)

def build_lexer(**kwargs):
	lexer = IndentLexer(**kwargs)
	return lexer