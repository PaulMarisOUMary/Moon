import argparse
import re

from pprint import pprint
from typing import Optional

from moon.lexer import build_lexer, print_tokens
from moon.parser import build_parser
from moon.interpreter import execute_program

def main():
    class TypedNamespace(argparse.Namespace):
        filename: str
        debug: Optional[bool]

    args_parser = argparse.ArgumentParser(description="Run the Moon script.")
    args_parser.add_argument("filename", help="Path to the Moon script file.", type=str)
    args_parser.add_argument("-d", "--debug", action="store_true", help="Enable debugging mode.")

    args = args_parser.parse_args(namespace=TypedNamespace())

    if args.filename is None:
        print("Usage: python3 moon.py <filename> [-d]")
        exit(1)

    with open(args.filename, 'r', encoding="utf-8") as f:
        source_code = f.read()

    # Remove any leading newline(s)
    source_code = source_code.lstrip('\n')
    # Replace groups of x4 whitespaces by a tabulation
    source_code = re.sub(
        pattern=r"^(\s{4})+",
        repl=lambda m: '\t' * (len(m.group(0)) // 4),
        string=source_code,
        flags=re.MULTILINE
    )

    lexer = build_lexer()
    lexer.input(source_code)

    if args.debug:
        print("===== Tokens =====")
        print_tokens(source_code)
        print("==================")

    parser = build_parser()
    parsed_code = parser.parse(source_code+'\n', lexer=lexer)

    if args.debug:
        print("=====  AST   =====")
        pprint(parsed_code)
        print("==================")

    execute_program(parsed_code)

if __name__ == "__main__":
    main()