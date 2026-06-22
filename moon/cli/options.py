from enum import Enum
from pathlib import Path
from typing import Annotated

from typer import Argument, Option


class StartRule(str, Enum):
    """Valid entrypoint rules accepted by the Moon grammar."""

    start = "start"
    file_input = "file_input"
    single_input = "single_input"
    eval_input = "eval_input"


FileArg = Annotated[
    Path,
    Argument(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to the .mn source file.",
    ),
]

StartOpt = Annotated[
    StartRule,
    Option(
        "--start",
        "-s",
        help="Entrypoint rule.",
    ),
]
