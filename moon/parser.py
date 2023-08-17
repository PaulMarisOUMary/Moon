import ply.yacc as yacc

from moon import tokens, build_lexer

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

# Program
def p_program(p):
    'program : statements'
    p[0] = p[1]

# Statements
def p_statements(p):
    '''statements : statements statement NEWLINE
                  | statements NEWLINE
                  | statement'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    elif len(p) == 3:
        p[0] = p[1]  # Ignore the newline token
    else:
        p[0] = [p[1]]

# Statement
def p_statement(p):
    '''statement : variable_declaration
                 | expression'''
    p[0] = p[1]

# Variable Declaration
def p_variable_declaration(p):
    'variable_declaration : IDENTIFIER IS expression'
    p[0] = ('variable_declaration', p[1], p[3])

# Expression rules
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EXPONENT expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('not', p[2])

def p_expression_relational(p):
    '''expression : expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression IS expression
                  | expression ISNT expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_literal(p):
    '''expression : INTEGER
                  | FLOAT
                  | STRING
                  | BOOLEAN
                  | NULL'''
    p[0] = p[1]

# Error handling
def p_error(p):
    print("Syntax error at '%s'" % p)

# Empty rule
def p_empty(p):
    'empty :'
    p[0] = None

def print_tokens(code):
    lexer = build_lexer()
    lexer.input(code)
    print('----- Tokens -----')
    for token in list(lexer):
        print(token)
    print('----- ERRORS -----')
    for error in lexer.errors:
        print(error)
    if not lexer.errors:
        print('No errors found')
    print('------------------')

# Main program
def parse_code(code):
    lexer = build_lexer()
    lexer.input(code)

    print_tokens(code)

    parser = yacc.yacc()
    result = parser.parse(code, lexer=lexer)

    return result