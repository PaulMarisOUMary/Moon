from typing import Optional
from typer import Argument, FileText, Option, Typer
from pprint import pprint

from . import __version__ as moon_version
from .lexer import build_lexer, print_tokens
from .parser import build_parser
from .interpreter import TEnvironment, execute_program


cli = Typer(
    help="Moon CLI",
    add_completion=False,
)


def run_code(
        source_code: str, 
        debug: bool,
        environment: Optional[TEnvironment] = None
    ):
    lexer = build_lexer()
    lexer.input(source_code)

    if debug:
        print("===== Tokens =====")
        print_tokens(source_code)
        print("==================")

    parser = build_parser()
    parsed_code = parser.parse(source_code+'\n', lexer=lexer)

    if debug:
        print("=====  AST   =====")
        pprint(parsed_code)
        print("==================")

    execute_program(parsed_code, environment=environment)

def start_playground(debug: bool):
    print(f"Moon interactive playground (v{moon_version})")
    print("Type Moon code. Finish a block with an empty line. Ctrl+C to exit.\n")

    environment = dict()

    while True:
        env_backup = environment.copy()
        try:
            lines = []
            while True:
                prompt = ">>> " if not lines else "... "
                line = input(prompt)
                if not line.rstrip() and lines:
                    break
                elif not line.rstrip():
                    continue
                lines.append(line)

            code_block = "\n".join(lines)
            run_code(code_block, debug, environment)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[error] {e}")
            environment = env_backup


@cli.callback(invoke_without_command=True)
def main(
    filename: Optional[FileText] = Argument(None, help="Path to the Moon script file."),
    debug: bool = Option(False, "-d", "--debug", help="Enable debugging mode.")
):
    if filename:
        with filename as f:
            source_code = f.read()
        run_code(source_code, debug)
    else:
        start_playground(debug)