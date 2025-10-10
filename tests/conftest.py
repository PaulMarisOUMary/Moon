import pytest

from pathlib import Path

from lark import Lark
from lark.indenter import PythonIndenter


class Indenter(PythonIndenter):
	NL_type = "_NEWLINE"
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = "_INDENT"
	DEDENT_type = "_DEDENT"
	tab_len = 4


@pytest.fixture(scope="session")
def parser():
    return Lark.open(
        grammar_filename=str(Path(__file__).parent.parent / "moon" / "grammar" / "moon.lark"),
        rel_to=__file__,
        parser="lalr",
        postlex=Indenter(),
        start="file_input",
        lexer="contextual"
    )