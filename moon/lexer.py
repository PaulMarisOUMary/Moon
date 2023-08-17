import ply.lex as lex

# A string containing ignored characters (spaces and tabs)
t_ignore = ' '

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EXPONENT = r'\*\*'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='

# Reserved words
reserved = {
	'action': 'ACTION',
	'and': 'AND',
	'as': 'AS',
	'assert': 'ASSERT', # ❌
	'async': 'ASYNC', # ❌
	'await': 'AWAIT', # ❌
	'continue': 'CONTINUE',
	'default': 'DEFAULT', # ❌
	'dict': 'DICT',
	'elif': 'ELIF', # ❌
	'else': 'ELSE',
	'end': 'END', # ❌
	'false': 'BOOLEAN',
	'fail': 'FAIL',
	'from': 'FROM',
	'for': 'FOR', # ❌
	'global': 'GLOBAL', # ❌
	'has': 'HAS',
	'if': 'IF',
	'in': 'IN', # ❌
	'is': 'IS',
	'isnt': 'ISNT',
	'lambda': 'LAMBDA', # ❌
	'list': 'LIST',
	'null': 'NULL',
	'not': 'NOT',
	'nothing': 'NOTHING', # ❌
	'or': 'OR',
	'pass': 'PASS', # ❌
	'raise': 'RAISE',
	'result': 'RESULT',
	'test': 'TEST',
	'thing': 'THING',
	'true': 'BOOLEAN',
	'use': 'USE',
	'stop': 'STOP',
	'while': 'WHILE',
	'yield': 'YIELD', # ❌
}

# List of token names
tokens = [
	'INBODY', 'ENDBODY',
	'TABULATION', 'NEWLINE',
	'COMMENT', 'MULTILINE_COMMENT',
	'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN',
	'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'EXPONENT',
	'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
] + list(reserved.values())

# Identifier rule
def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
	return t

# Floating-point literal rule
def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

# Integer literal rule
def t_INTEGER(t):
	r'\b(0|[1-9][0-9]*)\b'
	t.value = int(t.value)
	return t

# String literal rule
def t_STRING(t):
	r'"(\\.|[^"\\])*"'
	t.value = t.value[1:-1]  # Remove the quotes
	return t

# Boolean literal rule
def t_BOOLEAN(t):
	r'\b(true|false)'
	t.value = (t.value == 'true')
	return t

# Comment rule for single-line comments
def t_COMMENT(t):
	r'\#[^\n]*'
	return t

# Comment rule for multi-line comments
def t_MULTILINE_COMMENT(t):
	r'\([\s\S]*?\)'
	t.lexer.lineno += t.value.count('\n')
	return t

def t_TABULATION(t):
	r'\t'
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t

# Error handling
def t_error(t):
	print(f"Illegal character '{t.value[0]}'")
	t.lexer.errors.append([t.value[0], t.lexer.lineno, t.lexer.lexpos])
	t.lexer.skip(1)

def build_lexer(**kwargs):
	lexer = IndentLexer(**kwargs)
	return lexer

class IndentLexer(object):
	def __init__(self, **kwargs) -> None:
		self.lexer = lex.lex(**kwargs)
		self.lexer.errors = []
		self.token_stream = None

	@property
	def errors(self):
		return self.lexer.errors

	def _new_token(self, type, lineno):
		tok = lex.LexToken()
		tok.type = type
		tok.value = None
		tok.lineno = lineno
		tok.lexpos = 0
		return tok

	def _indentation_filter(self, tokens):
		indentation_stack = [0]
		current_indentation = 0
		indentation_count = 0

		for token in tokens:
			if token.type == 'NEWLINE':
				indentation_count = 0
				yield token
			elif token.type == 'TABULATION':
				indentation_count += 1
				continue  # Continue to the next token
			else:
				current_indentation = indentation_count
				# Check for an increase in indentation
				if current_indentation > indentation_stack[-1]:
					for _ in range(current_indentation - indentation_stack[-1]):
						yield self._new_token('INBODY', token.lineno)
					indentation_stack.append(current_indentation)
				# Check for a decrease in indentation
				elif current_indentation < indentation_stack[-1]:
					for _ in range(indentation_stack[-1] - current_indentation):
						yield self._new_token('ENDBODY', token.lineno)
						indentation_stack.pop()
				yield token

		# Handle any remaining dedentation at the end of the file
		for _ in range(indentation_stack[-1]):
			yield self._new_token('ENDBODY', token.lineno if token else 0)


	def _indent_tokens(self, lexer):
		token = None
		tokens = iter(lexer.token, None)
		for token in self._indentation_filter(tokens):
			yield token

	def input(self, data):
		self.lexer.input(data)
		self.token_stream = self._indent_tokens(self.lexer)

	def __iter__(self):
		return self.token_stream
	
	def __list__(self):
		return self.token_stream

	def token(self):
		try:
			return next(self.token_stream)
		except StopIteration:
			return None