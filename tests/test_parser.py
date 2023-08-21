import pytest

from moon.lexer import build_lexer
from moon.parser import build_parser

def parse_code(code):
    lexer = build_lexer()
    lexer.input(code)

    parser = build_parser()
    return parser.parse(code+'\n', lexer=lexer)

# Literals
@pytest.mark.parametrize("input_code, expected_output", [
    ("1", [('integer_literal', 1)]),
    ("1.0", [('float_literal', 1.0)]),
    ("\"Hello World\"", [('string_literal', "Hello World")]),
    ("true", [('boolean_literal', True)]),
    ("false", [('boolean_literal', False)]),
    ("null", [('null_literal', 'null')]),
])
def test_literals(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Expressions

# Arithmetic expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 + 1", [('arithmetic_expression', '+', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 - 1", [('arithmetic_expression', '-', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 * 1", [('arithmetic_expression', '*', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 / 1", [('arithmetic_expression', '/', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 % 1", [('arithmetic_expression', '%', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 ** 1", [('arithmetic_expression', '**', ('integer_literal', 1), ('integer_literal', 1))]),

])
def test_arithmetic_expressions(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Comparison expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 < 1", [('comparison_expression', '<', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 <= 1", [('comparison_expression', '<=', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 > 1", [('comparison_expression', '>', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 >= 1", [('comparison_expression', '>=', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 is 1", [('comparison_expression', '==', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 isnt 1", [('comparison_expression', '!=', ('integer_literal', 1), ('integer_literal', 1))]),
])
def test_comparison_expressions(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Logical expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("true and true", [('logical_expression', 'and', ('boolean_literal', True), ('boolean_literal', True))]),
    ("true or true", [('logical_expression', 'or', ('boolean_literal', True), ('boolean_literal', True))]),
    ("not true", [('logical_expression', 'not', ('boolean_literal', True))]),
])
def test_logical_expressions(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Unary expressions
"""MISSING"""

# Grouping expressions
"""MISSING"""

# Statements

# Variable declaration statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 1", [('variable_declaration_statement', 'x', ('integer_literal', 1))]),
])
def test_variable_declaration_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# If statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("if true\n\t1", [('if_statement', ('boolean_literal', True), [('integer_literal', 1)], None)]),
    ("if true\n\tif false\n\t\t1", [
        ('if_statement', ('boolean_literal', True), [
            ('if_statement', ('boolean_literal', False), [
                ('integer_literal', 1)
            ], None)
        ], None)
    ]),
    ("if true\n\tif false\n\t\tvariable is 3\n\t\tif true\n\t\t\tvariable is 5\n\t\tvariable is 6", 
        [('if_statement', ('boolean_literal', True),
            [('if_statement', ('boolean_literal', False), 
                [('variable_declaration_statement', 'variable', ('integer_literal', 3)),
                ('if_statement', ('boolean_literal', True),
                [('variable_declaration_statement', 'variable', ('integer_literal', 5))], None),
                ('variable_declaration_statement', 'variable', ('integer_literal', 6))], None)],
            None)]
    ),
])
def test_if_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# If else statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("if true\n\t1\nelse\n\t2", [('if_statement', ('boolean_literal', True), [('integer_literal', 1)], [('integer_literal', 2)])]),
    ("if true\n\t1\nelse\n\tif false\n\t\t2\n\telse\n\t\t3", [
        ('if_statement', ('boolean_literal', True), [
            ('integer_literal', 1)
        ], [
            ('if_statement', ('boolean_literal', False), [
                ('integer_literal', 2)
            ], [
                ('integer_literal', 3)
            ])
        ])
    ]),
])
def test_if_else_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# While statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("while true\n\t1", [('while_statement', ('boolean_literal', True), [('integer_literal', 1)])]),
    ("while true\n\t1\nwhile false or true\n\t2\n\twhile true\n\t\twhile true\n\t\t\t3\n\t4", [
	('while_statement', ('boolean_literal', True), [
		('integer_literal', 1)]), 
	('while_statement', ('logical_expression', 'or', ('boolean_literal', False), ('boolean_literal', True)), [
		('integer_literal', 2), 
		('while_statement', ('boolean_literal', True), [
			('while_statement', ('boolean_literal', True), [
				('integer_literal', 3)
				])
			]), 
		('integer_literal', 4)
	])
]),
])
def test_while_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Break statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("stop\n", [('break_statement',)]),
])
def test_break_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Continue statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("skip\n", [('continue_statement',)]),
])
def test_continue_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Action statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("action x\n\t1", [('action_statement', 'x', [], [('integer_literal', 1)])]),
    ("action x y\n\t1", [('action_statement', 'x', ['y'], [('integer_literal', 1)])]),
    ("action x y z\n\t1", [('action_statement', 'x', ['y', 'z'], [('integer_literal', 1)])]),
    ("action x\n\t1\n\taction y a b\n\t\t2\n\t\t3\n\t\taction z\n\t\t\t4\n\t5", [
        ('action_statement', 'x', [], [
            ('integer_literal', 1),
            ('action_statement', 'y', ['a', 'b'], [
                ('integer_literal', 2),
                ('integer_literal', 3),
                ('action_statement', 'z', [], [
                    ('integer_literal', 4)
                ])
            ]),
            ('integer_literal', 5)
        ])
    ]),
])
def test_action_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Call statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("call x\n", [('call_statement', 'x', [])]),
    ("call x y\n", [('call_statement', 'x', ['y'])]),
    ("call x 1 z\n", [('call_statement', 'x', [('integer_literal', 1), 'z'])]),
])
def test_call_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Return statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("result\n", [('return_statement', [])]),
    ("result 1\n", [('return_statement', [('integer_literal', 1)])]),
    ("result 1 2\n", [('return_statement', [('integer_literal', 1), ('integer_literal', 2)])]),
])
def test_return_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Print statements
@pytest.mark.parametrize("input_code, expected_output", [
    ("print\n", [('print_statement', [])]),
    ("print 1\n", [('print_statement', [('integer_literal', 1)])]),
    ("print 1 2\n", [('print_statement', [('integer_literal', 1), ('integer_literal', 2)])]),
])
def test_print_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Call assignement to variable
@pytest.mark.parametrize("input_code, expected_output", [
    ("x is call y\n", [('variable_declaration_statement', 'x', ('call_statement', 'y', []))]),
    ("x is call y 1\n", [('variable_declaration_statement', 'x', ('call_statement', 'y', [('integer_literal', 1)]))]),
    ("x is call y 1 2\n", [('variable_declaration_statement', 'x', ('call_statement', 'y', [('integer_literal', 1), ('integer_literal', 2)]))]),
])
def test_call_assignment_to_variable(input_code, expected_output):
    assert parse_code(input_code) == expected_output
