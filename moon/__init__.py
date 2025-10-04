from importlib.metadata import version, PackageNotFoundError
from pkgutil import extend_path


__title__ = "moon"
__author__ = "PaulMarisOUMary"
__license__ = "CC BY-NC-SA 4.0"
__copyright__ = "Copyright 2023-present PaulMarisOUMary"

try:
    __version__ = version("moon")
except PackageNotFoundError:
    __version__ = "0.0.0"
__path__ = extend_path(__path__, __name__)


from .lexer import build_lexer, tokens, print_tokens
from .parser import build_parser
from .interpreter import execute_program