import pytest

from moon.lexer import build_lexer
from moon.parser import build_parser
from moon.interpreter import execute_program

def code_to_output(code):
    code = code.lstrip('\n')

    lexer = build_lexer()
    lexer.input(code)

    parser = build_parser()
    parsed_code = parser.parse(code+'\n', lexer=lexer)

    execute_program(parsed_code)

@pytest.mark.parametrize("input_code, expected_output", [
    ("print 1", "1"),
    ("print 1.0", "1.0"),
    ("print \"Hello World\"", "Hello World"),
    ("print true", "True"),
    ("print false", "False"),
    ("print null", "None"),
])
def test_print_statement(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("print 1 + 1", "2"),
    ("print 1 - 1", "0"),
    ("print 1 * 1", "1"),
    ("print 1 / 1", "1.0"),
    ("print 1 % 1", "0"),
    ("print 1 ** 1", "1"),
])
def test_arithmetic_expressions(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("print 1 < 1", "False"),
    ("print 1 <= 1", "True"),
    ("print 1 > 1", "False"),
    ("print 1 >= 1", "True"),
    ("print 1 is 1", "True"),
    ("print 1 isnt 1", "False"),
])
def test_comparison_expressions(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("print true and true", "True"),
    ("print true or true", "True"),
    ("print not true", "False"),
])
def test_logical_expressions(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("print 5 + 5 * 5", "30"),
    ("print 5 + 5 / 5", "6.0"),
    ("print 5 + 5 % 5", "5"),
    ("print 5 + 5 ** 5", "3130"),
])
def test_arithmetic_expressions_precedence(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 5\nprint x", "5"),
    ("x is 5\ny is 6\nprint x + y", "11"),
    ("x is 5\ny is 6\nprint x + y * 5", "35"),
])
def test_variable_declaration_statements(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("print true and false", "False"),
    ("print false or true", "True"),
    ("print not false", "True"),
    ("print false isnt true", "True"),
    ("print true is true", "True"),
])
def test_boolean_literals(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("if true\n\tprint \"True block\"\nprint \"Outside if\"", "True block\nOutside if"),
    ("if false\n\tprint \"False block\"\nprint \"Outside if\"", "Outside if"),
])
def test_if_statements(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 0\nwhile x < 5\n\tx is x + 1\nprint x", "5"),
])
def test_while_statements(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output

@pytest.mark.parametrize("input_code, expected_output", [
    ("x is 0\nwhile x < 5\n\tx is x + 1\n\tstop\nprint x", "1"),
    ("x is 0\nwhile true\n\tprint x\n\tx is x + 1\n\tif x > 5\n\t\tif x is 10\n\t\t\tstop", "0\n1\n2\n3\n4\n5\n6\n7\n8\n9"),
    ("x is 0\nwhile true\n\tx is x + 1\n\tif x is 3\n\t\tskip\n\tprint x\n\n\tif x is 10\n\t\tstop", "1\n2\n4\n5\n6\n7\n8\n9\n10"),
])
def test_break_statements(input_code, expected_output, capsys):
    code_to_output(input_code)

    captured = capsys.readouterr()

    assert captured.out.rstrip() == expected_output