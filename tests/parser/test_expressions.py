import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "eval_input"


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
@assert_ast_structure(START)
def test_parser_arithmetic_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


COMPARISON_EXPRESSIONS = (
    ("1 < 2", "comp_expr(integer_literal(1), comp_operator(<), integer_literal(2))"),
    ("1 <= 2", "comp_expr(integer_literal(1), comp_operator(<=), integer_literal(2))"),
    ("1 > 2", "comp_expr(integer_literal(1), comp_operator(>), integer_literal(2))"),
    ("1 >= 2", "comp_expr(integer_literal(1), comp_operator(>=), integer_literal(2))"),
    ("1 is 2", "comp_expr(integer_literal(1), comp_operator(is), integer_literal(2))"),
    ("1 isnt 2", "comp_expr(integer_literal(1), comp_operator(isnt), integer_literal(2))"),
)
@pytest.mark.parametrize("source, expected_ast", [*COMPARISON_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_comparison_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


LOGICAL_EXPRESSIONS = (
    ("false and true", "and_expr(false_literal, and, true_literal)"),
    ("false or true", "or_expr(false_literal, or, true_literal)"),
    ("not true", "not_expr(not, true_literal)"),
)
@pytest.mark.parametrize("source, expected_ast", [*LOGICAL_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_logical_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


TERNARY_EXPRESSIONS = (
    ("x if true else y", "expression(var(identifier(x)), true_literal, var(identifier(y)))"),
    ("x if a else y if b else z", "expression(var(identifier(x)), var(identifier(a)), expression(var(identifier(y)), var(identifier(b)), var(identifier(z))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*TERNARY_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_ternary_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


PRECEDENCE_EXPRESSIONS = (
    ("1 + 2 * 3", "arith_expr(integer_literal(1), add_operator(+), term(integer_literal(2), mul_operator(*), integer_literal(3)))"),
    ("2 ** 3 ** 2", "power(integer_literal(2), **, power(integer_literal(3), **, integer_literal(2)))"),
    ("not true and false", "and_expr(not_expr(not, true_literal), and, false_literal)"),
    ("1 < 2 < 3", "comp_expr(integer_literal(1), comp_operator(<), integer_literal(2), comp_operator(<), integer_literal(3))"),
    ("1 + 2 < 3 and true", "and_expr(comp_expr(arith_expr(integer_literal(1), add_operator(+), integer_literal(2)), comp_operator(<), integer_literal(3)), and, true_literal)"),
)
@pytest.mark.parametrize("source, expected_ast", [*PRECEDENCE_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_precedence_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


UNARY_SIGN_EXPRESSIONS = (
    ("-1", "integer_literal(-1)"),
    ("-1.5", "float_literal(-1.5)"),
    ("- 1", "factor(unary_operator(-), integer_literal(1))"),
    ("- 1.5", "factor(unary_operator(-), float_literal(1.5))"),
    ("-x", "factor(unary_operator(-), var(identifier(x)))"),
    ("- x", "factor(unary_operator(-), var(identifier(x)))"),
    ("--x", "factor(unary_operator(-), factor(unary_operator(-), var(identifier(x))))"),
    ("+x", "factor(unary_operator(+), var(identifier(x)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*UNARY_SIGN_EXPRESSIONS])
@assert_ast_structure(START)
def test_parser_unary_sign_expressions(moon_parser: Lark, source: str, expected_ast: str) -> None: ...