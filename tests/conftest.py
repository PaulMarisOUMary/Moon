import pytest

from lark import Lark

from moon import build_parser

@pytest.fixture(scope="session")
def moon_parser() -> Lark:
    return build_parser()