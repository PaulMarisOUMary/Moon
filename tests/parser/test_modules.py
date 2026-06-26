import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


USE_NAME_STATEMENTS = (
    ("use mymodule", "use_statement(use_name(identifier(mymodule)))"),
)
@pytest.mark.parametrize("source, expected_ast", [*USE_NAME_STATEMENTS])
@assert_ast_structure(START)
def test_parser_use_name_statements(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


USE_FROM_NAMED_IMPORT = (
    ('from "math.mn" use sqrt', 'use_statement(use_from("math.mn", use_target(identifier(sqrt))))'),
    ('from "math.mn" use sqrt as sq', 'use_statement(use_from("math.mn", use_target(identifier(sqrt), use_as(identifier(sq)))))'),
)
@pytest.mark.parametrize("source, expected_ast", [*USE_FROM_NAMED_IMPORT])
@assert_ast_structure(START)
def test_parser_use_from_named_import(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


USE_FROM_WILDCARD_IMPORT = (
    ('from "math.mn" use *', 'use_statement(use_from("math.mn", *))'),
)
@pytest.mark.parametrize("source, expected_ast", [*USE_FROM_WILDCARD_IMPORT])
@assert_ast_structure(START)
def test_parser_use_from_wildcard_import(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


USE_FROM_DOTTED_PATH = (
    ("from mod use x", "use_statement(use_from(dotted_path(identifier(mod)), use_target(identifier(x))))"),
    ("from math.geometry use sqrt", "use_statement(use_from(dotted_path(identifier(math), identifier(geometry)), use_target(identifier(sqrt))))"),
    ("from math.geometry.deep use x", "use_statement(use_from(dotted_path(identifier(math), identifier(geometry), identifier(deep)), use_target(identifier(x))))"),
    ("from math.geometry use *", "use_statement(use_from(dotted_path(identifier(math), identifier(geometry)), *))"),
)
@pytest.mark.parametrize("source, expected_ast", [*USE_FROM_DOTTED_PATH])
@assert_ast_structure(START)
def test_parser_use_from_dotted_path(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


USE_WILDCARD_ALIAS_INVALID = (
    'from "math.mn" use * as m',
    "from math.geometry use * as g",
)
@pytest.mark.parametrize("source", [*USE_WILDCARD_ALIAS_INVALID])
@assert_parse_error(START)
def test_parser_use_wildcard_alias_invalid(moon_parser: Lark, source: str) -> None: ...


USE_STATEMENT_INVALID = (
    "use mymodule as m",
    "use math.geometry",
    'from "math.mn" use sqrt as sq as another',
)
@pytest.mark.parametrize("source", [*USE_STATEMENT_INVALID])
@assert_parse_error(START)
def test_parser_use_statement_invalid(moon_parser: Lark, source: str) -> None: ...