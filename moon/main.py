import sys

from moon.lexer import build_lexer, print_tokens
from moon.parser import build_parser
from moon.interpreter import execute_program

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 moon.py <filename>")
        exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        source_code = f.read()

    lexer = build_lexer()
    lexer.input(source_code)

    # print_tokens(source_code)

    parser = build_parser()
    parsed_code = parser.parse(source_code+'\n', lexer=lexer)

    # print(parsed_code)

    execute_program(parsed_code)

if __name__ == "__main__":
    main()