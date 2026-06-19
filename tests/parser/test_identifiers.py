import pytest

from lark import Lark

from .utils import assert_ast_structure


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