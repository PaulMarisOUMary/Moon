import pytest

from lark import Lark

from .utils import assert_ast_structure, assert_parse_error


START = "file_input"


THING_ATTRIBUTES = (
    (
        "thing Dog\n    has name\n",
        "thing_statement(identifier(Dog), thing_suite(attribute(identifier(name))))",
    ),
    (
        "thing Dog\n    has name\n    has age\n",
        "thing_statement(identifier(Dog), thing_suite(attribute(identifier(name)), attribute(identifier(age))))",
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*THING_ATTRIBUTES])
@assert_ast_structure(START)
def test_parser_thing_attributes(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


THING_INHERITANCE = (
    (
        "thing Dog is Animal\n    has name\n",
        "thing_statement(identifier(Dog), inheritance(is, identifier(Animal)), thing_suite(attribute(identifier(name))))",
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*THING_INHERITANCE])
@assert_ast_structure(START)
def test_parser_thing_inheritance(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


THING_WITH_METHODS = (
    (
        'thing Dog\n    action bark\n        print "woof"\n',
        'thing_statement(identifier(Dog), thing_suite(action_statement(identifier(bark), parameters, suite(builtin_call(builtin_name(print), arguments(string_literal("woof")))))))',
    ),
    (
        'thing Dog is Animal\n    has name\n    action bark\n        print "woof"\n',
        'thing_statement(identifier(Dog), inheritance(is, identifier(Animal)), thing_suite(attribute(identifier(name)), action_statement(identifier(bark), parameters, suite(builtin_call(builtin_name(print), arguments(string_literal("woof")))))))',
    ),
    (
        'thing Dog\n    has name\n    action bark\n        print "woof"\n    action fetch\n        result "ball"\n',
        'thing_statement(identifier(Dog), thing_suite(attribute(identifier(name)), action_statement(identifier(bark), parameters, suite(builtin_call(builtin_name(print), arguments(string_literal("woof"))))), action_statement(identifier(fetch), parameters, suite(result_statement(string_literal("ball"))))))',
    ),
)
@pytest.mark.parametrize("source, expected_ast", [*THING_WITH_METHODS])
@assert_ast_structure(START)
def test_parser_thing_with_methods(moon_parser: Lark, source: str, expected_ast: str) -> None: ...


THING_INVALID = (
    "thing Dog\n",
    "thing Dog is\n    has name\n",
)
@pytest.mark.parametrize("source", [*THING_INVALID])
@assert_parse_error(START)
def test_parser_thing_invalid(moon_parser: Lark, source: str) -> None: ...