import pytest

from lark import Tree
from pathlib import Path

from moon.parser import parse


START = "file_input"

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
EXAMPLE_FILES = sorted(EXAMPLES_DIR.glob("*.mn"))


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.name)
def test_example_parses_without_error(path: Path) -> None:
    source = path.read_text()
    tree = parse(source, start=START)

    assert isinstance(tree, Tree)
    assert tree.data == "file_input"
    assert len(tree.children) > 0


def test_examples_directory_is_not_empty() -> None:
    assert len(EXAMPLE_FILES) > 0