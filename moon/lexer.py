import ply.lex as lex

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
	'COMMENT', 'MULTILINE_COMMENT', 'TABULATION', 'NEWLINE',
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
	return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' '

def t_TABULATION(t):
	r'\t+'
	#t.lexer.lineno += len(t.value)
	return t

# Newline handling
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
	lexer = lex.lex(**kwargs)
	lexer.errors = []
	return lexer

# Test the lexer
if __name__ == "__main__":
	data = '''# comment here
(
	another comment here
)

variable is (sneaky comment) 5

(action addNumbers a b
	comment that contains a keyword etc)

action addNumbers a b
	result a + b
sum is addNumbers 1 2
print sum
(
'''
	lexer = build_lexer()

	lexer.input(data)
	for token in lexer:
		print(token)

	print(lexer.errors)