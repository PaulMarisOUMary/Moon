import pytest

from moon.lexer import build_lexer
from moon.parser import build_parser

def parse_code(code):
    lexer = build_lexer()
    lexer.input(code)

    parser = build_parser()
    return parser.parse(code+'\n', lexer=lexer)

# Literals

## Integer
@pytest.mark.parametrize("input_code, expected_output", [
    ("0", [("integer_literal", 0)]),
    ("4096", [("integer_literal", 4096)]),
])
def test_integer_literal(input_code, expected_output):
    assert parse_code(input_code) == expected_output
## Float
@pytest.mark.parametrize("input_code, expected_output", [
    ("0.0001", [("float_literal", 0.0001)]),
    ("1.4096", [("float_literal", 1.4096)]),
    ("-4.4096", [("float_literal", -4.4096)]),
])
def test_float_literal(input_code, expected_output):
    assert parse_code(input_code) == expected_output
## String
@pytest.mark.parametrize("input_code, expected_output", [
    ("\"Hello World\"", [("string_literal", "Hello World")]),
    ("'Hello World'", [("string_literal", "Hello World")]),
])
def test_string_literal(input_code, expected_output):
    assert parse_code(input_code) == expected_output
## Boolean
@pytest.mark.parametrize("input_code, expected_output", [
    ("true", [("boolean_literal", True)]),
    ("false", [("boolean_literal", False)]),
])
def test_boolean_literal(input_code, expected_output):
    assert parse_code(input_code) == expected_output
## Null
@pytest.mark.parametrize("input_code, expected_output", [
    ("null", [("null_literal",)]),
])
def test_null_literal(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Composite

## Lists
@pytest.mark.parametrize("input_code, expected_output", [
    ("list", [("list_composite", [])]),
    ("list\n\t0", [("list_composite", [("integer_literal", 0)])]),
    ("list\n\t1\n\t2\n\t3\n\t4\n\t5\n\tlist\n\t\t'a'\n\t\t'b'\n\t\tlist\n\t\t\ttrue\n\t\t\tfalse\n\t\t'c'\n\t\t'd'", [
        ("list_composite", [
            ("integer_literal", 1),
            ("integer_literal", 2),
            ("integer_literal", 3),
            ("integer_literal", 4),
            ("integer_literal", 5),
            ("list_composite", [
                ("string_literal", 'a'),
                ("string_literal", 'b'),
                ("list_composite", [
                    ("boolean_literal", True),
                    ("boolean_literal", False)
                ]),
                ("string_literal", 'c'),
                ("string_literal", 'd')
            ])
        ])
    ]),
])
def test_composite_lists(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Dict

# Expressions

## Arithmetic
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 + 2", [("arithmetic_expression", '+', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 - 2", [("arithmetic_expression", '-', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 * 2", [("arithmetic_expression", '*', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 / 2", [("arithmetic_expression", '/', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 % 2", [("arithmetic_expression", '%', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 ** 2", [("arithmetic_expression", "**", ("integer_literal", 1), ("integer_literal", 2))]),
])
def test_arithmetic_expression(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Comparison
@pytest.mark.parametrize("input_code, expected_output", [
    ("1 < 2", [("comparison_expression", '<', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 <= 2", [("comparison_expression", "<=", ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 > 2", [("comparison_expression", '>', ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 >= 2", [("comparison_expression", ">=", ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 is 2", [("comparison_expression", "==", ("integer_literal", 1), ("integer_literal", 2))]),
    ("1 isnt 2", [("comparison_expression", "!=", ("integer_literal", 1), ("integer_literal", 2))]),
])
def test_comparison_expression(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Logical
@pytest.mark.parametrize("input_code, expected_output", [
    ("true and false", [("logical_expression", "and", ("boolean_literal", True), ("boolean_literal", False))]),
    ("true or false", [("logical_expression", "or", ("boolean_literal", True), ("boolean_literal", False))]),
    ("not true", [("logical_expression", "not", ("boolean_literal", True))]),
])
def test_logical_expression(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Call
@pytest.mark.parametrize("input_code, expected_output", [
    ("call func_name", [("call", "func_name", [])]),
    ("call func_name 1 2 3 4", [("call", "func_name", [("integer_literal", 1), ("integer_literal", 2), ("integer_literal", 3), ("integer_literal", 4)])]),
])
def test_call(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Ask
@pytest.mark.parametrize("input_code, expected_output", [
    ("ask", [("ask", [])]),
    ("ask 'prompt'", [("ask", [("string_literal", "prompt")])]),
    ("ask 'prompt' 'prompt 2'", [("ask", [("string_literal", "prompt"), ("string_literal", "prompt 2")])]),
])
def test_ask(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Statement

## Variable Assignment
@pytest.mark.parametrize("input_code, expected_output", [
    # Literals assignment
    ("var is null", [("variable_declaration_statement", "var", ("null_literal",))]),
    ("var is false", [("variable_declaration_statement", "var", ("boolean_literal", False))]),
    ("var is true", [("variable_declaration_statement", "var", ("boolean_literal", True))]),
    ("var is 1", [("variable_declaration_statement", "var", ("integer_literal", 1))]),
    ("var is 1.1", [("variable_declaration_statement", "var", ("float_literal", 1.1))]),
    ("var is 'str'", [("variable_declaration_statement", "var", ("string_literal", "str"))]),
    # Arithmetic
    ("var is 1 + 2", [("variable_declaration_statement", "var", ("arithmetic_expression", '+', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 - 2", [("variable_declaration_statement", "var", ("arithmetic_expression", '-', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 * 2", [("variable_declaration_statement", "var", ("arithmetic_expression", '*', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 / 2", [("variable_declaration_statement", "var", ("arithmetic_expression", '/', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 % 2", [("variable_declaration_statement", "var", ("arithmetic_expression", '%', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 ** 2", [("variable_declaration_statement", "var", ("arithmetic_expression", "**", ("integer_literal", 1), ("integer_literal", 2)))]),
    # Comparison
    ("var is 1 < 2", [("variable_declaration_statement", "var", ("comparison_expression", '<', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 <= 2", [("variable_declaration_statement", "var", ("comparison_expression", "<=", ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 > 2", [("variable_declaration_statement", "var", ("comparison_expression", '>', ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 >= 2", [("variable_declaration_statement", "var", ("comparison_expression", ">=", ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 is 2", [("variable_declaration_statement", "var", ("comparison_expression", "==", ("integer_literal", 1), ("integer_literal", 2)))]),
    ("var is 1 isnt 2", [("variable_declaration_statement", "var", ("comparison_expression", "!=", ("integer_literal", 1), ("integer_literal", 2)))]),
    # Logical
    ("var is true and false", [("variable_declaration_statement", "var", ("logical_expression", "and", ("boolean_literal", True), ("boolean_literal", False)))]),
    ("var is true or false", [("variable_declaration_statement", "var", ("logical_expression", "or", ("boolean_literal", True), ("boolean_literal", False)))]),
    ("var is not true", [("variable_declaration_statement", "var", ("logical_expression", "not", ("boolean_literal", True)))]),
    # Call
    ("var is call func_name", [("variable_declaration_statement", "var", ("call", "func_name", []))]),
    ("var is call func_name 1 2", [("variable_declaration_statement", "var", ("call", "func_name", [("integer_literal", 1), ("integer_literal", 2)]))]),
    # Ask
    ("var is ask", [("variable_declaration_statement", "var", ("ask", []))]),
    ("var is ask 'prompt'", [("variable_declaration_statement", "var", ("ask", [("string_literal", "prompt")]))]),
    ("var is ask 'prompt' 'prompt 2'", [("variable_declaration_statement", "var", ("ask", [("string_literal", "prompt"), ("string_literal", "prompt 2")]))]),
])
def test_variable_declaration_statement(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Stop
@pytest.mark.parametrize("input_code, expected_output", [
    ("stop", [("stop_statement",)]),
])
def test_stop_statement(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Skip
@pytest.mark.parametrize("input_code, expected_output", [
    ("skip", [("skip_statement",)]),
])
def test_skip_statement(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Result
@pytest.mark.parametrize("input_code, expected_output", [
    ("result", [("result_statement", [])]),
    ("result 1", [("result_statement", [("integer_literal", 1)])]),
    ("result 1 2", [("result_statement", [("integer_literal", 1), ("integer_literal", 2)])]),
])
def test_result_statement(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Print
@pytest.mark.parametrize("input_code, expected_output", [
    ("print", [("print_statement", [])]),
    ("print 1", [("print_statement", [("integer_literal", 1)])]),
    ("print 1 2", [("print_statement", [("integer_literal", 1), ("integer_literal", 2)])]),
])
def test_print_statement(input_code, expected_output):
    assert parse_code(input_code) == expected_output

# Statements

## If
@pytest.mark.parametrize("input_code, expected_output", [
    ("if true\n\tprint 1", [("ifelse_statements", ("boolean_literal", True), [("print_statement",[("integer_literal", 1)])], None)]),
    ("if true\n\tprint 1\n\tprint 2", [("ifelse_statements", ("boolean_literal", True), [("print_statement",[("integer_literal", 1)]), ("print_statement",[("integer_literal", 2)])], None)]),
])
def test_if_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("if true\n\tprint 1\nelse\n\tprint 2", [("ifelse_statements", ("boolean_literal", True), [("print_statement", [("integer_literal", 1)])], [("print_statement", [("integer_literal", 2)])])]),
    ("if true\n\tprint 1\n\tprint 2\nelse\n\tprint 3\n\tprint 4", [("ifelse_statements", ("boolean_literal", True), [("print_statement", [("integer_literal", 1)]), ("print_statement", [("integer_literal", 2)])], [("print_statement", [("integer_literal", 3)]), ("print_statement", [("integer_literal", 4)])])]),
])
def test_ifelse_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## While
@pytest.mark.parametrize("input_code, expected_output", [
    ("while true\n\tprint 1", [("while_statements", ("boolean_literal", True), [("print_statement", [("integer_literal", 1)])])]),
    ("while true\n\tprint 1\n\tprint 2", [("while_statements", ("boolean_literal", True), [("print_statement", [("integer_literal", 1)]), ("print_statement", [("integer_literal", 2)])])]),
])
def test_while_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output

## Action
@pytest.mark.parametrize("input_code, expected_output", [
    ("action func_name\n\tprint 1", [("action_statements", "func_name", [], [("print_statement", [("integer_literal", 1)])])]),
    ("action func_name\n\tprint 1\n\tprint 2", [("action_statements", "func_name", [], [("print_statement", [("integer_literal", 1)]), ("print_statement", [("integer_literal", 2)])])]),
    ("action func_name a\n\tprint 1", [("action_statements", "func_name", ['a'], [("print_statement", [("integer_literal", 1)])])]),
    ("action func_name a b\n\tprint 1", [("action_statements", "func_name", ['a', 'b'], [("print_statement", [("integer_literal", 1)])])]),
    ("action func_name a b\n\tprint 1\n\tprint 2", [("action_statements", "func_name", ['a', 'b'], [("print_statement", [("integer_literal", 1)]), ("print_statement", [("integer_literal", 2)])])]),
])
def test_action_statements(input_code, expected_output):
    assert parse_code(input_code) == expected_output