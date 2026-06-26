import pytest

from lark import Lark

from .utils import assert_ast_structure


START = "file_input"


FILE_INPUT_EMPTY_OR_BLANK = (
    ('', ''),
    ('\n', ''),
    ("\n\n", ''),
    ('\t', ''),
    ("\t\t", ''),
    ("\t\n", ''),
    ("\t\t\n", ''),
    ('   ', ''),
    ("  \n  \n", ''),
)
@pytest.mark.parametrize("source, expected_ast", [*FILE_INPUT_EMPTY_OR_BLANK])
@assert_ast_structure(START)
def test_parser_file_input_empty_or_blank(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


FILE_INPUT_COMPOSITION = (
    ("x is 1\ny is 2\n", "assign_statement(identifier(x), is, integer_literal(1)), assign_statement(identifier(y), is, integer_literal(2))"),
    ("stop\nskip\n...\n", "stop_statement, skip_statement, noop_statement"),
)
@pytest.mark.parametrize("source, expected_ast", [*FILE_INPUT_COMPOSITION])
@assert_ast_structure(START)
def test_parser_file_input_composition(moon_parser: Lark, source: str, expected_ast: str) -> None: ...