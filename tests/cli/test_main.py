from typer.testing import CliRunner

from moon.cli import app

from .conftest import normalize_output


runner = CliRunner()


def test_root_help_lists_subcommands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "ast" in normalize_output(result.output)
    assert "run" in normalize_output(result.output)


def test_root_without_arguments_shows_missing_command() -> None:
    result = runner.invoke(app, [])

    assert result.exit_code != 0


def test_unknown_subcommand_is_rejected() -> None:
    result = runner.invoke(app, ["not_a_real_command"])

    assert result.exit_code != 0
