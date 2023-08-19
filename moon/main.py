import argparse

from pprint import pprint

from moon.lexer import build_lexer, print_tokens
from moon.parser import build_parser
from moon.interpreter import execute_program

def main():
    args_parser = argparse.ArgumentParser(description="Run the Moon script.")
    args_parser.add_argument("filename", help="Path to the Moon script file.")
    args_parser.add_argument("-d", "--debug", action="store_true", help="Enable debugging mode.")

    args = args_parser.parse_args()

    if args.filename is None:
        print("Usage: python3 moon.py <filename> [-d]")
        exit(1)

    with open(args.filename, "r") as f:
        source_code = f.read()

    source_code = source_code.lstrip('\n')

    lexer = build_lexer()
    lexer.input(source_code)

    if args.debug:
        print("===== Tokens =====")
        print_tokens(source_code)
        print("==================")

    parser = build_parser()
    parsed_code = parser.parse(source_code+'\n', lexer=lexer)

    if args.debug:
        print("=====   AST   =====")
        pprint(parsed_code)
        print("==================")


    execute_program(parsed_code)

if __name__ == "__main__":
    main()