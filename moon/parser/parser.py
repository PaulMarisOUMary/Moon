from typing import Any
from pathlib import Path

from lark import Lark, Tree
from lark.indenter import Indenter


LARK_FILE = Path("grammar/moon.lark")
REL_PATH = Path(__file__).parent


class MoonIndenter(Indenter):
	NL_type = "_NEWLINE"
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = "_INDENT"
	DEDENT_type = "_DEDENT"
	tab_len = 4


def build_parser(
	grammar_filename: str = str(LARK_FILE),
	rel_to: str = str(REL_PATH),
	*args: Any,
	**kwargs: Any,
	) -> Lark:
		return Lark.open(
			grammar_filename=grammar_filename,
			rel_to=rel_to,
			parser="lalr",
			postlex=MoonIndenter(),
			start=["start", "file_input", "single_input", "eval_input"],
			lexer="contextual",
			*args,
			**kwargs,
		)


def parse(
	source: str,
	start: str = "file_input",
	**kwargs: Any
	) -> Tree:
	parser = build_parser()
	if not source.endswith('\n'):
		source += '\n'
	return parser.parse(source, start=start, **kwargs)