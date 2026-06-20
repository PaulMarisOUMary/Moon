import pytest

from lark import Lark
from lark.exceptions import LarkError

from .utils import assert_ast_structure, assert_parse_error


START = "single_input"


SINGLE_INPUT_VALID = (
    ('\n', ''),
    ("   \n", ""),
    ("x is 5\n", "assign_statement(identifier(x), is, integer_literal(5))"),
    ("stop\n", "stop_statement"),
    ("while true\n    print 1\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("if true\n    print 1\n", "if_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
    ("action foo\n    result 1\n", "action_statement(identifier(foo), parameters, suite(result_statement(integer_literal(1))))"),
    ("while true\n    print 1\n\n", "while_statement(true_literal, suite(builtin_call(builtin_name(print), arguments(integer_literal(1)))))"),
)
@pytest.mark.parametrize("source, expected_ast", [*SINGLE_INPUT_VALID])
@assert_ast_structure(START)
def test_parser_single_input_valid(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


SINGLE_INPUT_INVALID = (
    "x is 5\ny is 6\n",
    "stop\nskip\n",
    "while true\n    x is 1\nstop\n",
)
@pytest.mark.parametrize("source", [*SINGLE_INPUT_INVALID])
@assert_parse_error(START)
def test_parser_single_input_invalid(moon_parser: Lark, source: str) -> None: ...


def test_parser_single_input_empty_is_invalid(moon_parser: Lark) -> None:
    with pytest.raises(LarkError):
        moon_parser.parse('', start=START)