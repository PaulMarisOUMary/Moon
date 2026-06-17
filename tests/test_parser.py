import pytest

from functools import wraps
from typing import Any, Callable

from lark import Lark, Token, Tree

from .utils import clean_type


def ast_to_str(node: Tree | Token | None, is_root: bool = False) -> str:
    if node is None:
        return ''

    if isinstance(node, Tree):
        rule_name = clean_type(node.data)
        children_strs = [
            ast_to_str(child)
            for child in node.children
            if child is not None
        ]

        ENTRYPOINTS = {"start", "file_input", "single_input", "eval_input"}
        if is_root and rule_name in ENTRYPOINTS:
            return ", ".join(children_strs)

        if not children_strs:
            return rule_name

        return f"{rule_name}({', '.join(children_strs)})"

    if isinstance(node, Token):
        return str(node.value)

    return str(node)


def assert_ast_structure(start: str = "file_input") -> Callable[..., Any]:
    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(moon_parser: Lark, source: str, *args: Any, **kwargs: Any) -> None:
            expected_ast: str = kwargs.get("expected_ast", args[0] if args else None)
            
            if expected_ast is None:
                raise ValueError(f"Test for source '{source}' did not provide an 'expected_ast'.")

            tree: Tree = moon_parser.parse(source, start=start)
            actual_ast = ast_to_str(tree, is_root=True)

            assert actual_ast == expected_ast, (
                f"\nIncorrect AST structure for '{source}' (start='{start}')\n"
                f"Expected : {expected_ast}\n"
                f"Got      : {actual_ast}"
            )

            return func(moon_parser, source, *args, **kwargs)
        return wrapper
    return decorator


VALID_FILE_INPUT = (
    ('', ''),
    ('\n', ''),
    ("\n\n", ''),
    ('\t', ''),
    ("\t\t", ''),
    ("\t\n", ''),
    ("\t\t\n", ''),
)
@pytest.mark.parametrize("source, expected_ast", [*VALID_FILE_INPUT])
@assert_ast_structure("file_input")
def test_parser_valid_file_input(moon_parser: Lark, source: str, expected_ast: str) -> None: ...

BOOLEAN_AND_NULL_LITERAL = (
    ("true", "true_literal"),
    ("false", "false_literal"),
    ("null", "null_literal"),
)
@pytest.mark.parametrize("source, expected_ast", [*BOOLEAN_AND_NULL_LITERAL])
@assert_ast_structure("eval_input")
def test_parser_boolean_and_null(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


INTEGER_LITERAL = (
    ('0', "integer_literal(0)"),
    ('1', "integer_literal(1)"),
    ("42", "integer_literal(42)"),
    ("4096", "integer_literal(4096)"),
    ('-0', "integer_literal(-0)"),
    ('-1', "integer_literal(-1)"),
    ("-42", "integer_literal(-42)"),
    ("-4096", "integer_literal(-4096)"),
    ('+0', "integer_literal(+0)"),
    ('+1', "integer_literal(+1)"),
    ("+42", "integer_literal(+42)"),
    ("+4096", "integer_literal(+4096)"),
)
@pytest.mark.parametrize("source, expected_ast", [*INTEGER_LITERAL])
@assert_ast_structure("eval_input")
def test_parser_integer_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


FLOAT_LITERAL = (
    ("0.0", "float_literal(0.0)"),
    ("0.00000000", "float_literal(0.00000000)"),
    ("1.1", "float_literal(1.1)"),
    (".0001", "float_literal(.0001)"),
    ("1e10", "float_literal(1e10)"),
    ("1E10", "float_literal(1E10)"),
    ("1e-10", "float_literal(1e-10)"),
    ("1E-10", "float_literal(1E-10)"),
    ("1e+10", "float_literal(1e+10)"),
    ("1E+10", "float_literal(1E+10)"),
    (".1e10", "float_literal(.1e10)"),
    (".1E10", "float_literal(.1E10)"),
    (".1e-10", "float_literal(.1e-10)"),
    (".1E-10", "float_literal(.1E-10)"),
    (".1e+10", "float_literal(.1e+10)"),
    (".1E+10", "float_literal(.1E+10)"),
    ("-0.0", "float_literal(-0.0)"),
    ("-0.00000000", "float_literal(-0.00000000)"),
    ("-1.1", "float_literal(-1.1)"),
    ("-.0001", "float_literal(-.0001)"),
    ("-1e10", "float_literal(-1e10)"),
    ("-1E10", "float_literal(-1E10)"),
    ("-1e-10", "float_literal(-1e-10)"),
    ("-1E-10", "float_literal(-1E-10)"),
    ("-1e+10", "float_literal(-1e+10)"),
    ("-1E+10", "float_literal(-1E+10)"),
    ("-.1e10", "float_literal(-.1e10)"),
    ("-.1E10", "float_literal(-.1E10)"),
    ("-.1e-10", "float_literal(-.1e-10)"),
    ("-.1E-10", "float_literal(-.1E-10)"),
    ("-.1e+10", "float_literal(-.1e+10)"),
    ("-.1E+10", "float_literal(-.1E+10)"),
    ("+0.0", "float_literal(+0.0)"),
    ("+0.00000000", "float_literal(+0.00000000)"),
    ("+1.1", "float_literal(+1.1)"),
    ("+.0001", "float_literal(+.0001)"),
    ("+1e10", "float_literal(+1e10)"),
    ("+1E10", "float_literal(+1E10)"),
    ("+1e-10", "float_literal(+1e-10)"),
    ("+1E-10", "float_literal(+1E-10)"),
    ("+1e+10", "float_literal(+1e+10)"),
    ("+1E+10", "float_literal(+1E+10)"),
    ("+.1e10", "float_literal(+.1e10)"),
    ("+.1E10", "float_literal(+.1E10)"),
    ("+.1e-10", "float_literal(+.1e-10)"),
    ("+.1E-10", "float_literal(+.1E-10)"),
    ("+.1e+10", "float_literal(+.1e+10)"),
    ("+.1E+10", "float_literal(+.1E+10)"),
)
@pytest.mark.parametrize("source, expected_ast", [*FLOAT_LITERAL])
@assert_ast_structure("eval_input")
def test_parser_float_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


STRING_LITERAL = (
    ('"string"', 'string_literal("string")'),
    ('""', 'string_literal("")'),
    ('"string with spaces"', 'string_literal("string with spaces")'),
    ('"string with (parens) {} []"', 'string_literal("string with (parens) {} []")'),
    ('"string with \\"quotes\\""', 'string_literal("string with \\"quotes\\"")'),
    ('"string with \\\\ backslash"', 'string_literal("string with \\\\ backslash")'),
    ('"string with \\n new line"', 'string_literal("string with \\n new line")'),
    ('"string with \\t tabulation"', 'string_literal("string with \\t tabulation")'),
    ('"string with \\u2600 unicode"', 'string_literal("string with \\u2600 unicode")'),
    ('"emoji 🍎"', 'string_literal("emoji 🍎")'),

    ("'string'", "string_literal('string')"),
    ("'string\\\\'", "string_literal('string\\\\')"),
    ("''", "string_literal('')"),
    ("'string with spaces'", "string_literal('string with spaces')"),
    ("'string with (parens) {} []'", "string_literal('string with (parens) {} []')"),
    ("'string with \\'quotes\\''", "string_literal('string with \\'quotes\\'')"),
    ("'string with \\\\ backslash'", "string_literal('string with \\\\ backslash')"),
    ("'string with \\n new line'", "string_literal('string with \\n new line')"),
    ("'string with \\t tabulation'", "string_literal('string with \\t tabulation')"),
    ("'string with \\u2600 unicode'", "string_literal('string with \\u2600 unicode')"),
    ("'emoji 🍎'", "string_literal('emoji 🍎')"),
)
@pytest.mark.parametrize("source, expected_ast", [*STRING_LITERAL])
@assert_ast_structure("eval_input")
def test_parser_string_literal(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


IDENTIFIER = (
    ('🍎', "var(identifier(🍎))"),
    ("apple", "var(identifier(apple))"),
    ("display_name", "var(identifier(display_name))"),
    ("Data_1", "var(identifier(Data_1))"),
    ("x", "var(identifier(x))"),
    ("X", "var(identifier(X))"),
    ("__private", "var(identifier(__private))"),
    ("A1234567890", "var(identifier(A1234567890))"),
    ("__init__", "var(identifier(__init__))"),
    ("a_", "var(identifier(a_))"),
    ("a_" * 50, f"var(identifier({'a_' * 50}))"),
    ('🧠', "var(identifier(🧠))"),
    ("truefalse", "var(identifier(truefalse))"),
    ("null0", "var(identifier(null0))"),
    ("action1", "var(identifier(action1))"),
)
@pytest.mark.parametrize("source, expected_ast", [*IDENTIFIER])
@assert_ast_structure("eval_input")
def test_parser_identifier(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


ARITHMETIC_EXPRESSIONS = (
    ("1 + 2", "arith_expr(integer_literal(1), add_operator(+), integer_literal(2))"),
    ("1 - 2", "arith_expr(integer_literal(1), add_operator(-), integer_literal(2))"),
    ("1 * 2", "term(integer_literal(1), mul_operator(*), integer_literal(2))"),
    ("1 / 2", "term(integer_literal(1), mul_operator(/), integer_literal(2))"),
    ("1 // 2", "term(integer_literal(1), mul_operator(//), integer_literal(2))"),
    ("1 % 2", "term(integer_literal(1), mul_operator(%), integer_literal(2))"),
    ("1 ** 2", "power(integer_literal(1), **, integer_literal(2))"),
)
@pytest.mark.parametrize("source, expected_ast", [*ARITHMETIC_EXPRESSIONS])
@assert_ast_structure("eval_input")
def test_parser_arithmetic_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


RELATIONAL_EXPRESSIONS = (
    ("1 < 2", "comp_expr(integer_literal(1), comp_operator(<), integer_literal(2))"),
    ("1 <= 2", "comp_expr(integer_literal(1), comp_operator(<=), integer_literal(2))"),
    ("1 > 2", "comp_expr(integer_literal(1), comp_operator(>), integer_literal(2))"),
    ("1 >= 2", "comp_expr(integer_literal(1), comp_operator(>=), integer_literal(2))"),
    ("1 is 2", "comp_expr(integer_literal(1), comp_operator(is), integer_literal(2))"),
    ("1 isnt 2", "comp_expr(integer_literal(1), comp_operator(isnt), integer_literal(2))"),
    ("false and true", "and_expr(false_literal, and, true_literal)"),
    ("false or true", "or_expr(false_literal, or, true_literal)"),
    ("not true", "not_expr(not, true_literal)"),
)
@pytest.mark.parametrize("source, expected_ast", [*RELATIONAL_EXPRESSIONS])
@assert_ast_structure("eval_input")
def test_parser_relational_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


TERNARY_EXPRESSIONS = (
    ("x if true else y", "expression(var(identifier(x)), if, true_literal, else, var(identifier(y)))"),
    ("x if a else y if b else z", "expression(var(identifier(x)), if, var(identifier(a)), else, expression(var(identifier(y)), if, var(identifier(b)), else, var(identifier(z))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*TERNARY_EXPRESSIONS])
@assert_ast_structure("eval_input")
def test_parser_ternary_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


CALL_EXPRESSIONS = (
    ("call my_func", "call_expr(call, identifier(my_func), arguments)"),
    ("call run 10", "call_expr(call, identifier(run), arguments(integer_literal(10)))"),
    ("call run 1 2 3", "call_expr(call, identifier(run), arguments(integer_literal(1), integer_literal(2), integer_literal(3)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*CALL_EXPRESSIONS])
@assert_ast_structure("eval_input")
def test_parser_call_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...