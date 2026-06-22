from typer import Option, echo

from .options import FileArg, StartOpt, StartRule


def view_ast(
    file: FileArg,
    start: StartOpt = StartRule.file_input,
    compact: bool = Option(
        False, "-c", help="Print stringified AST instead of a tree shape."
    ),
) -> None:
    echo(f"Parsing {file.name} to view AST (compact={compact})...")
