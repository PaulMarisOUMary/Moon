from pathlib import Path

from lark import Lark
from lark.indenter import Indenter


LARK_FILE = Path("grammar/moon.lark")


class MoonIndenter(Indenter):
	NL_type = "_NEWLINE"
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = "_INDENT"
	DEDENT_type = "_DEDENT"
	tab_len = 4


def build_parser(
	grammar_filename: str = str(LARK_FILE),
	*args,
	**kwargs,
	) -> Lark:
		return Lark.open(
			grammar_filename=grammar_filename,
			rel_to=__file__,
			parser="lalr",
			postlex=MoonIndenter(),
			start=["start", "file_input", "eval_input"],
			*args,
			**kwargs,
		)