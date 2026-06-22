import sys

from typer import Typer
from typer.main import get_command


def _known_commands(app: Typer) -> set[str]:
    click_app = get_command(app)
    return set(getattr(click_app, "commands", {}).keys())


def _passthrough_flags(app: Typer) -> set[str]:
    click_app = get_command(app)
    ctx = click_app.make_context(
        info_name=click_app.name or "moon",
        args=[],
        resilient_parsing=True,
    )
    flags: set[str] = set()
    for param in click_app.get_params(ctx):
        flags.update(param.opts)
        flags.update(param.secondary_opts)
    return flags


def inject_default_command(app: Typer, default: str = "run") -> None:
    args = sys.argv[1:]

    if not args:
        return

    first = args[0]

    if first in _known_commands(app) or first in _passthrough_flags(app):
        return

    sys.argv.insert(1, default)
