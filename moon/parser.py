import ply.yacc as yacc

from lexer import tokens, build_lexer

precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('right', 'NOT'),
	('nonassoc', 'IS', 'ISNT'),
	('nonassoc', 'LT', 'LE', 'GT', 'GE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
	('right', 'EXPONENT'),
)

def p_program(p):
	"""program : statements"""
	p[0] = p[1]

def p_statements(p):
	"""statements : statements statement
				  | statement"""
	if len(p) == 3:
		p[0] = p[1] + [p[2]]
	else:
		p[0] = [p[1]]

def p_statement(p):
	"""statement : expression NEWLINE
				 | compound_statement"""
	p[0] = p[1]

def p_compound_statement(p):
	"""compound_statement : LIST NEWLINE INBODY statements ENDBODY"""
	p[0] = ('list', [x for x in p[4] if x is not None])

def p_expression(p):
	"""expression : INTEGER
				  | compound_statement"""
	p[0] = p[1]

def p_error(p):
	print("Syntax error at '%s'" % p.value)

def print_tokens(code):
	lexer = build_lexer()
	lexer.input(code)
	print('----- Tokens -----')
	for token in lexer:
		print(token)
	print('----- ERRORS -----')
	for error in lexer.errors:
		print(error)
	if not lexer.errors:
		print('No errors found')
	print('------------------')

# Main program
def parse_code(code):
	code += '\n'
	lexer = build_lexer()
	lexer.input(code)

	print_tokens(code)

	parser = yacc.yacc()
	result = parser.parse(code+'\n', lexer=lexer)

	return result

if __name__ == '__main__':
	code = """list
	1
	2
	list
		3
		list
			4
	5
"""
	result = parse_code(code)
	print(result)
		
[
	('list', [
		1,
		2,
		('list', [
			3,
			('list', [
				4
				])
			])
		]),
		5
]