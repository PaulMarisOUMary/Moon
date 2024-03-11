import ply.yacc as yacc
from ply.yacc import YaccProduction as TYP

from .lexer import tokens, LexTokenT

# REMINDER: (value) in Python is not a tuple; (value,) is a tuple

tokens = tokens

precedence = (
	("left", "OR"),
	("left", "AND"),
	("right", "NOT"),
	("nonassoc", "LT", "LE", "GT", "GE"),
	("left", "PLUS", "MINUS"),
	("left", "MULTIPLY", "DIVIDE", "MODULO"),
	("right", "EXPONENT"),
)

def p_program(p: TYP):
	"""program : statements"""
	p[0] = p[1]

# Statements

def p_statements(p: TYP):
	"""statements : statements statement
				  | statement"""
	if len(p) == 3:
		p[0] = p[1] + [p[2]]
	else:
		p[0] = [p[1]]

def p_suite(p: TYP):
	"""suite : NEWLINE INDENT statements DEDENT"""
	p[0] = p[3]

## If / Else

def p_ifelse_statements(p: TYP):
	"""ifelse_statements : IF expression suite optional_else"""
	p[0] = ("ifelse_statements", p[2], p[3], (p[4] if len(p) == 5 else None))

def p_optional_else(p: TYP):
	"""optional_else : ELSE suite
					 | empty"""
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = None

## While

def p_while_statements(p: TYP):
	"""while_statements : WHILE expression suite"""
	p[0] = ("while_statements", p[2], p[3])

## Action

def p_optional_inline_params(p: TYP):
	"""optional_inline_params : IDENTIFIER optional_inline_params
							  | empty"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []

def p_action_statements(p: TYP):
	"""action_statements : ACTION IDENTIFIER optional_inline_params suite"""
	p[0] = ("action_statements", p[2], p[3], p[4])

## Composite

def p_list_composite(p: TYP):
	"""list_composite : LIST suite
					  | LIST NEWLINE"""

	p[0] = ("list_composite", p[2] if not p[2] == '\n' else [])

# Statement

def p_statement(p: TYP):
	"""statement : expression NEWLINE
				 | stop_statement NEWLINE
				 | skip_statement NEWLINE
				 | result_statement NEWLINE
				 | print_statement NEWLINE
				 | variable_declaration_statement
				 | ifelse_statements
				 | while_statements
				 | action_statements
				 | list_composite"""
	p[0] = p[1]

def p_optional_inline_args(p: TYP):
	"""optional_inline_args : expression optional_inline_args
							| empty"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []

def p_variable_declaration_statement(p: TYP):
	"""variable_declaration_statement : IDENTIFIER IS expression NEWLINE
									  | IDENTIFIER IS list_composite"""
	p[0] = ("variable_declaration_statement", p[1], p[3])

def p_stop_statement(p: TYP):
	"""stop_statement : STOP"""
	p[0] = ("stop_statement", )

def p_skip_statement(p: TYP):
	"""skip_statement : SKIP"""
	p[0] = ("skip_statement", )

def p_result_statement(p: TYP):
	"""result_statement : RESULT optional_inline_args"""
	p[0] = ("result_statement", p[2])

def p_print_statement(p: TYP):
	"""print_statement : PRINT optional_inline_args"""
	p[0] = ("print_statement", p[2])

# Expressions

def p_expression(p: TYP):
	"""expression : literals
				  | arithmetic_expression
				  | comparison_expression
				  | logical_expression
				  | call
				  | ask
				  | IDENTIFIER"""
	p[0] = p[1]

## Call

def p_call(p: TYP):
	"""call : CALL IDENTIFIER optional_inline_args"""
	p[0] = ("call", p[2], p[3])

## Ask

def p_ask(p: TYP):
	"""ask : ASK optional_inline_args"""
	p[0] = ("ask", p[2])

## Arithmetic, Comparison & Logical - Expressions

def p_arithmetic_expression(p: TYP):
	"""arithmetic_expression : expression PLUS expression
							 | expression MINUS expression
							 | expression MULTIPLY expression
							 | expression DIVIDE expression
							 | expression MODULO expression
							 | expression EXPONENT expression"""
	p[0] = ("arithmetic_expression", p[2], p[1], p[3])

def p_comparison_expression(p: TYP):
	"""comparison_expression : expression LT expression
							 | expression LE expression
							 | expression IS expression
							 | expression ISNT expression
							 | expression GT expression
							 | expression GE expression"""
	if p[2] == "is":
		p[2] = "=="
	elif p[2] == "isnt":
		p[2] = "!="
	p[0] = ("comparison_expression", p[2], p[1], p[3])

def p_logical_expression(p: TYP):
	"""logical_expression : expression AND expression
						  | expression OR expression
						  | NOT expression"""
	if len(p) == 4:
		p[0] = ("logical_expression", p[2], p[1], p[3])
	else:
		p[0] = ("logical_expression", p[1], p[2])

## Literals

def p_literals(p: TYP):
	"""literals : integer_literal
				| float_literal
				| string_literal
				| boolean_literal
				| null_literal"""
	p[0] = p[1]

def p_integer_literal(p: TYP):
	"""integer_literal : INTEGER"""
	p[0] = ("integer_literal", p[1])

def p_integer_float(p: TYP):
	"""float_literal : FLOAT"""
	p[0] = ("float_literal", p[1])

def p_integer_string(p: TYP):
	"""string_literal : STRING"""
	p[0] = ("string_literal", p[1])

def p_integer_boolean(p: TYP):
	"""boolean_literal : BOOLEAN"""
	p[0] = ("boolean_literal", p[1])

def p_integer_null(p: TYP):
	"""null_literal : NULL"""
	p[0] = ("null_literal",)

# Empty

def p_empty(p: TYP):
	"""empty :"""
	pass

# Error

def p_error(p: LexTokenT):
	if p:
		print(f"! ParserError: {p}")
	else:
		print("! Syntax error at EOF")



# ===== END OF PARSER =====

def build_parser():
	return yacc.yacc()