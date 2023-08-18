import pytest

from moon import parse_code

# Literals
@pytest.mark.parametrize("input_code, expected_output", [
    ("1", [('integer_literal', 1)]),
    ("1.0", [('float_literal', 1.0)]),
    ("\"Hello World\"", [('string_literal', "Hello World")]),
    ("true", [('boolean_literal', 'true')]),
    ("false", [('boolean_literal', 'false')]),
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
    ("1 is 1", [('comparison_expression', 'is', ('integer_literal', 1), ('integer_literal', 1))]),
    ("1 isnt 1", [('comparison_expression', 'isnt', ('integer_literal', 1), ('integer_literal', 1))]),
])
def test_comparison_expressions(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Logical expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("true and true", [('logical_expression', 'and', ('boolean_literal', 'true'), ('boolean_literal', 'true'))]),
    ("true or true", [('logical_expression', 'or', ('boolean_literal', 'true'), ('boolean_literal', 'true'))]),
    ("not true", [('logical_expression', 'not', ('boolean_literal', 'true'))]),
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
    ("if true\n\t1", [('if_statement', ('boolean_literal', 'true'), [('integer_literal', 1)])]),
    ("if true\n\tif false\n\t\t1", [
        ('if_statement', ('boolean_literal', 'true'), [
            ('if_statement', ('boolean_literal', 'false'), [
                ('integer_literal', 1)
            ])
        ])
    ]),
    ("if true\n\tif false\n\t\tvariable is 3\n\t\tif true\n\t\t\tvariable is 5\n\t\tvariable is 6", [
        ('if_statement', ('boolean_literal', 'true'), [
            ('if_statement', ('boolean_literal', 'false'), [
                ('variable_declaration_statement', 'variable', ('integer_literal', 3)),
                ('if_statement', ('boolean_literal', 'true'), [
                    ('variable_declaration_statement', 'variable', ('integer_literal', 5))
                ]),
                ('variable_declaration_statement', 'variable', ('integer_literal', 6))
            ])
        ])
    ]),
])
def test_if_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# While statements
@pytest.mark.parametrize("input_code, expected_output", [
])
def test_while_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output