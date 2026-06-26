from typer import echo, prompt, secho, Abort, Exit
from typer.colors import RED, BRIGHT_BLUE

from .options import FileArg, StartOpt, StartRule

from ..moon import run as run_file, Session
from ..runtime import NULL


def run(file: FileArg, start: StartOpt = StartRule.file_input) -> None:
    secho(f"Executing {file.name} using entrypoint '{start.value}'...", fg=BRIGHT_BLUE)
    try:
        content = file.read_text("utf-8")
        run_file(content)
    except FileNotFoundError:
        secho(f"Error: File '{file}' not found.", fg=RED, err=True)
        raise Exit(1)
    except Exception as e:
        secho(f"Error: {e}", fg=RED, err=True)
        raise Exit(1)


def repl() -> None:
    session = Session()
    secho("Moon REPL - Press Ctrl+C or Ctrl+D to exit", fg=BRIGHT_BLUE)
    while True:
        try:
            source = prompt("(>", prompt_suffix=' ')
        except (Abort, EOFError, KeyboardInterrupt):
            secho("\nBye.", fg=BRIGHT_BLUE)
            break

        source = source.strip()
        if not source:
            continue

        try:
            result = session.eval_expr(source)
            if result is not NULL:
                echo(result)
        except Exception as e:
            secho(f"Error: {e}", fg=RED, err=True)
