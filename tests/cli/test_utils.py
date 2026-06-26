import sys

import pytest

from moon.cli import app
from moon.cli.utils import _known_commands, _passthrough_flags, inject_default_command


@pytest.fixture(autouse=True)
def restore_argv():
    original = list(sys.argv)
    yield
    sys.argv[:] = original


def test_known_commands_includes_registered_subcommands() -> None:
    known = _known_commands(app)

    assert "run" in known
    assert "ast" in known


def test_passthrough_flags_includes_help() -> None:
    flags = _passthrough_flags(app)

    assert "--help" in flags


def test_injects_default_when_first_arg_is_unknown() -> None:
    sys.argv = ["moon", "main.mn"]

    inject_default_command(app)

    assert sys.argv == ["moon", "run", "main.mn"]


def test_does_not_inject_for_known_subcommand() -> None:
    sys.argv = ["moon", "ast", "main.mn", "-c"]

    inject_default_command(app)

    assert sys.argv == ["moon", "ast", "main.mn", "-c"]


def test_does_not_inject_for_run_subcommand() -> None:
    sys.argv = ["moon", "run", "main.mn"]

    inject_default_command(app)

    assert sys.argv == ["moon", "run", "main.mn"]


def test_does_not_inject_for_help_flag() -> None:
    sys.argv = ["moon", "--help"]

    inject_default_command(app)

    assert sys.argv == ["moon", "--help"]


def test_does_not_inject_when_no_arguments() -> None:
    sys.argv = ["moon"]

    inject_default_command(app)

    assert sys.argv == ["moon"]


def test_injects_default_when_option_precedes_filename() -> None:
    sys.argv = ["moon", "--start", "eval_input", "main.mn"]

    inject_default_command(app)

    assert sys.argv == ["moon", "run", "--start", "eval_input", "main.mn"]


def test_custom_default_command_name() -> None:
    sys.argv = ["moon", "main.mn"]

    inject_default_command(app, default="run")

    assert sys.argv[1] == "run"
