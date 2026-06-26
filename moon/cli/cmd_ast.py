from typer import Option, secho
from typer.colors import YELLOW

from .options import FileArg, StartOpt, StartRule


def view_ast(
    file: FileArg,
    start: StartOpt = StartRule.file_input,
    compact: bool = Option(
        False, "-c", help="Print stringified AST instead of a tree shape."
    ),
) -> None:
    secho(
        f"Parsing {file.name} to view AST (compact={compact})...\nNot available.",
        fg=YELLOW,
    )
