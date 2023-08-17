import pytest

from moon import parse_code

#Test Arithmetic Expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 + 1", [('+', 1, 1)]),
    ("2 - 1", [('-', 2, 1)]),
    ("3 * 3", [('*', 3, 3)]),
    ("4 / 2", [('/', 4, 2)]),
    ("5 % 2", [('%', 5, 2)]),
    ("2 ** 3", [('**', 2, 3)])
])
def test_arithmetic_expressions(input_code, expected_output):

    pc = parse_code(input_code)
    print(pc, type(pc), type(expected_output), input_code)

    assert pc == expected_output

# Test Logical Expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("true and true", [('and', 'true', 'true')]),    # AND
    ("false and false", [('and', 'false', 'false')]),
    ("false and true", [('and', 'false', 'true')]),
    ("true and false", [('and', 'true', 'false')]),
    ("true or true", [('or', 'true', 'true')]),     # OR
    ("false or false", [('or', 'false', 'false')]),
    ("false or true", [('or', 'false', 'true')]),
    ("true or false", [('or', 'true', 'false')]),
    ("not false", [('not', 'false')]),        # NOT
    ("not true", [('not', 'true')]),
])
def test_logical_expressions(input_code, expected_output):
    pc = parse_code(input_code)

    print(pc, type(pc), type(expected_output), input_code)

    assert parse_code(input_code) == expected_output

# Test Relational Expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 < 2", [('<', 1, 2)]),
    ("2 <= 2", [('<=', 2, 2)]),
    ("3 > 1", [('>', 3, 1)]),
    ("4 >= 5", [('>=', 4, 5)]),
    ("5 is 5", [('is', 5, 5)]),
    ("6 isnt 6", [('isnt', 6, 6)]),
])
def test_relational_expressions(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Variables Declaration
@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 10", [('variable_declaration', 'x', 10)]),
    ("""u is true
v is false
w is null
x is 5
y is 0.55
z is "Hello World"
""", [
    ('variable_declaration', 'u', 'true'),
    ('variable_declaration', 'v', 'false'),
    ('variable_declaration', 'w', 'null'),
    ('variable_declaration', 'x', 5),
    ('variable_declaration', 'y', 0.55),
    ('variable_declaration', 'z', "Hello World"),
    ]),
])
def test_variables_declaration(input_code, expected_output):

    result = parse_code(input_code)
    print(result)

    assert result == expected_output

# Variable Declaration with Arithmetic Expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 1 + 1", [('variable_declaration', 'x', ('+', 1, 1))]),
    ("x is 2 - 1", [('variable_declaration', 'x', ('-', 2, 1))]),
    ("x is 3 * 3", [('variable_declaration', 'x', ('*', 3, 3))]),
    ("x is 4 / 2", [('variable_declaration', 'x', ('/', 4, 2))]),
    ("x is 5 % 2", [('variable_declaration', 'x', ('%', 5, 2))]),
    ("x is 2 ** 3", [('variable_declaration', 'x', ('**', 2, 3))]),
])
def test_variable_declaration_with_arithmetic_expressions(input_code, expected_output):
    pc = parse_code(input_code)
    print(pc, type(pc), type(expected_output), input_code)

    assert pc == expected_output

# Variable Declaration with Logical Expressions
@pytest.mark.parametrize("input_code, expected_output", [
    ("x is true and true", [('variable_declaration', 'x', ('and', 'true', 'true'))]),
    ("x is false and false", [('variable_declaration', 'x', ('and', 'false', 'false'))]),
    ("x is false and true", [('variable_declaration', 'x', ('and', 'false', 'true'))]),
    ("x is true and false", [('variable_declaration', 'x', ('and', 'true', 'false'))]),
    ("x is true or true", [('variable_declaration', 'x', ('or', 'true', 'true'))]),
    ("x is false or false", [('variable_declaration', 'x', ('or', 'false', 'false'))]),
    ("x is false or true", [('variable_declaration', 'x', ('or', 'false', 'true'))]),
    ("x is true or false", [('variable_declaration', 'x', ('or', 'true', 'false'))]),
    ("x is not false", [('variable_declaration', 'x', ('not', 'false'))]),
    ("x is not true", [('variable_declaration', 'x', ('not', 'true'))]),
])
def test_variable_declaration_with_logical_expressions(input_code, expected_output):
    pc = parse_code(input_code)
    print(pc, type(pc), type(expected_output), input_code)

    assert pc == expected_output