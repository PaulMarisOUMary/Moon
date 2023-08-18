import ply.yacc as yacc

from pprint import pprint

from .lexer import tokens, build_lexer

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
				 | if_statement
				 | while_statement
				 | break_statement
				 | continue_statement
				 | action_statement
				 | result_statement
				 | call_statement
				 | print_statement"""
	p[0] = p[1]

def p_if_statement(p):
	"""if_statement : IF conditional_test suite"""
	p[0] = ('if_statement', p[2], p[3])

def p_while_statement(p):
	"""while_statement : WHILE conditional_test suite"""
	p[0] = ('while_statement', p[2], p[3])

def p_action_statement(p):
	"""action_statement : ACTION IDENTIFIER optional_params suite"""
	p[0] = ('action_statement', p[2], p[3], p[4])

def p_call_statement(p):
    """call_statement : CALL IDENTIFIER optional_call_params"""
    p[0] = ('call_statement', p[2], p[3])

def p_optional_params(p):
	"""optional_params : IDENTIFIER optional_params
					   | empty"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []

def p_optional_call_params(p):
	"""optional_call_params : expression optional_call_params
					   		| empty"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []

def p_suite(p):
	"""suite : NEWLINE INDENT statements DEDENT"""
	p[0] = p[3]

def p_line(p):
	"""line : variable_declaration_statement
			| expression"""
	p[0] = p[1]

def p_variable_declaration_statement(p):
    """variable_declaration_statement : IDENTIFIER IS expression"""
    p[0] = ('variable_declaration_statement', p[1], p[3])

def p_conditional_test(p):
	"""conditional_test : comparison_expression
			   | logical_expression
			   | arithmetic_expression
			   | boolean_literal
			   | null_literal"""
	p[0] = p[1]

def p_literals(p):
	"""literals : integer_literal
			   | float_literal
			   | string_literal
			   | boolean_literal
			   | null_literal"""
	p[0] = p[1]

def p_interger_literal(p):
	"""integer_literal : INTEGER"""
	p[0] = ('integer_literal', p[1])

def p_float_literal(p):
	"""float_literal : FLOAT"""
	p[0] = ('float_literal', p[1])

def p_string_literal(p):
	"""string_literal : STRING"""
	p[0] = ('string_literal', p[1])

def p_boolean_literal(p):
	"""boolean_literal : BOOLEAN"""
	p[0] = ('boolean_literal', p[1])

def p_null_literal(p):
	"""null_literal : NULL"""
	p[0] = ('null_literal', p[1])

def p_expression(p):
	"""expression : literals
				  | comparison_expression
				  | arithmetic_expression
				  | logical_expression
				  | call_statement
				  | IDENTIFIER"""
	p[0] = p[1]

def p_comparison_expression(p):
	"""comparison_expression : expression LT expression
							 | expression LE expression
							 | expression IS expression
							 | expression ISNT expression
							 | expression GT expression
							 | expression GE expression"""
	p[0] = ('comparison_expression', p[2], p[1], p[3])

def p_arithmetic_expression(p):
	"""arithmetic_expression : expression PLUS expression
							 | expression MINUS expression
							 | expression MULTIPLY expression
							 | expression DIVIDE expression
							 | expression MODULO expression
							 | expression EXPONENT expression"""
	p[0] = ('arithmetic_expression', p[2], p[1], p[3])

def p_logical_expression(p):
	"""logical_expression : expression AND expression
						  | expression OR expression
						  | NOT expression"""
	# Add the appropriate action here, depending on the logical operator
	if len(p) == 4:
		p[0] = ('logical_expression', p[2], p[1], p[3])
	else:
		p[0] = ('logical_expression', p[1], p[2])

def p_break_statement(p):
	"""break_statement : STOP NEWLINE"""
	p[0] = ('break_statement',)

def p_continue_statement(p):
	"""continue_statement : CONTINUE NEWLINE"""
	p[0] = ('continue_statement',)

def p_result(p):
	"""result_statement : RESULT optional_results NEWLINE
						| RESULT NEWLINE"""
	if len(p) == 4:
		p[0] = ('return_statement', p[2])
	else:
		p[0] = ('return_statement', [])

def p_optional_result(p):
	"""optional_results : expression optional_results
					   | expression"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = [p[1]]

def p_print_statement(p):
	"""print_statement : PRINT optional_prints NEWLINE
					   | PRINT NEWLINE"""
	if len(p) == 4:
		p[0] = ('print_statement', p[2])
	else:
		p[0] = ('print_statement', [])

def p_optional_prints(p):
	"""optional_prints : expression optional_prints
					   | expression"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = [p[1]]

def p_empty(p):
	"""empty :"""
	pass

def p_error(p):
	if p:
		print("Syntax error at '%s'" % p.value)
	else:
		print("Syntax error at EOF")

def print_tokens(code):
	lexer = build_lexer()
	lexer.input(code)
	print('----- Tokens -----')
	for token in lexer: # type: ignore
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
	code = """variable is call a 1 2 3"""
	result = parse_code(code)
	pprint(result, indent=4)