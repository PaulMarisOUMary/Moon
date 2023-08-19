__title__ = 'moon'
__author__ = 'PaulMarisOUMary'
__license__ = 'CC BY-NC-SA 4.0'
__copyright__ = 'Copyright 2023-present PaulMarisOUMary'
__version__ = '0.0.0a'

from .main import main

from .lexer import build_lexer, tokens, print_tokens
from .parser import build_parser
from .interpreter import execute_program