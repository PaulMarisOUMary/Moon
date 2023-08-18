import ply.yacc as yacc

from lexer import tokens, build_lexer

precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('right', 'NOT'),
	('nonassoc', 'LT', 'LE', 'GT', 'GE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
	('right', 'EXPONENT'),
)

# The program is composed of 'statements'
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
	"""statement : line NEWLINE
				 | if_statement"""
	p[0] = p[1]

def p_if_statement(p):
	"""if_statement : IF literal suite"""
	p[0] = ('if_statement', p[2], p[3])

def p_suite(p):
	"""suite : NEWLINE INDENT statements DEDENT"""
	p[0] = p[3]

def p_line(p):
	"""line : assignment
			| literal"""
	p[0] = p[1]

def p_assignment(p):
	"""assignment : IDENTIFIER IS literal"""
	p[0] = ('variable_assignation', p[1], p[3])

def p_literal(p):
	"""literal : INTEGER
			   | FLOAT
			   | STRING
			   | BOOLEAN
			   | NULL"""
	p[0] = p[1]

def p_error(p):
	if p:
		print("Syntax error at '%s'" % p.value)
	else:
		print("Syntax error at EOF")

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
def parse_code(code: str):
	code = code.lstrip('\n')+'\n'
	lexer = build_lexer()
	lexer.input(code)

	print_tokens(code)

	parser = yacc.yacc()
	result = parser.parse(code+'\n', lexer=lexer)

	return result

if __name__ == '__main__':
	code = """
variable is 5
if 1
	if 2
		variable is 3
		if 4
			variable is 5
		variable is 6
x is 5"""
	result = parse_code(code)
	print('R', result)