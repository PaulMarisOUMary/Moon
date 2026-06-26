from pathlib import Path

from typer.testing import CliRunner

from moon.cli import app

from .conftest import normalize_output


runner = CliRunner()


def test_run_with_default_start(source_file: Path) -> None:
    result = runner.invoke(app, ["run", str(source_file)])

    assert result.exit_code == 0
    output = normalize_output(result.output)
    assert source_file.name in output
    assert "file_input" in output


def test_run_with_explicit_start(source_file: Path) -> None:
    result = runner.invoke(app, ["run", str(source_file), "--start", "eval_input"])

    assert result.exit_code == 0
    assert "eval_input" in normalize_output(result.output)


def test_run_with_short_start_flag(source_file: Path) -> None:
    result = runner.invoke(app, ["run", str(source_file), "-s", "single_input"])

    assert result.exit_code == 0
    assert "single_input" in normalize_output(result.output)


def test_run_rejects_invalid_start_value(source_file: Path) -> None:
    result = runner.invoke(app, ["run", str(source_file), "--start", "not_a_real_rule"])

    assert result.exit_code != 0
    assert "not_a_real_rule" in normalize_output(result.output)


def test_run_rejects_missing_file() -> None:
    result = runner.invoke(app, ["run", "this_file_does_not_exist.mn"])

    assert result.exit_code != 0
    assert "does not exist" in normalize_output(result.output)


def test_run_rejects_missing_file_argument() -> None:
    result = runner.invoke(app, ["run"])

    assert result.exit_code != 0


def test_run_help() -> None:
    result = runner.invoke(app, ["run", "--help"])

    assert result.exit_code == 0
    assert "--start" in normalize_output(result.output)


def test_run_option_before_argument(source_file: Path) -> None:
    result = runner.invoke(app, ["run", "--start", "eval_input", str(source_file)])

    assert result.exit_code == 0
    assert "eval_input" in normalize_output(result.output)