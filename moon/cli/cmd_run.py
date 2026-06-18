from typer import echo

from .options import FileArg, StartOpt, StartRule


def run(file: FileArg, start: StartOpt = StartRule.file_input) -> None:
    echo(f"Executing {file.name} using entrypoint '{start.value}'...")