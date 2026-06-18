from typer import Typer

from .cmd_ast import view_ast
from .cmd_run import run
from .utils import inject_default_command


app = Typer(
    name="moon",
    help="Moon Language Interpreter CLI",
    add_completion=False,
)


app.command(
    name="ast",
    help="Inspect and debug Moon's Abstract Syntax Tree (AST).",
)(view_ast)

app.command(
    name="run",
    help="Run and evaluate Moon source files.",
)(run)


inject_default_command(app)