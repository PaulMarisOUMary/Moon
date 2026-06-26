from pathlib import Path

from typer.testing import CliRunner

from moon.cli import app

from .conftest import normalize_output


runner = CliRunner()


def test_ast_default(source_file: Path) -> None:
    result = runner.invoke(app, ["ast", str(source_file)])

    assert result.exit_code == 0
    assert source_file.name in normalize_output(result.output)
    assert "compact=False" in normalize_output(result.output)


def test_ast_compact_flag_before_file(source_file: Path) -> None:
    result = runner.invoke(app, ["ast", "-c", str(source_file)])

    assert result.exit_code == 0
    assert "compact=True" in normalize_output(result.output)


def test_ast_compact_flag_after_file(source_file: Path) -> None:
    result = runner.invoke(app, ["ast", str(source_file), "-c"])

    assert result.exit_code == 0
    assert "compact=True" in normalize_output(result.output)


def test_ast_with_start_option(source_file: Path) -> None:
    result = runner.invoke(app, ["ast", str(source_file), "--start", "single_input"])

    assert result.exit_code == 0


def test_ast_rejects_invalid_start_value(source_file: Path) -> None:
    result = runner.invoke(app, ["ast", str(source_file), "--start", "garbage"])

    assert result.exit_code != 0


def test_ast_rejects_missing_file() -> None:
    result = runner.invoke(app, ["ast", "this_file_does_not_exist.mn", "-c"])

    assert result.exit_code != 0
    assert "does not exist" in normalize_output(result.output)


def test_ast_help() -> None:
    result = runner.invoke(app, ["ast", "--help"])

    assert result.exit_code == 0
    assert "-c" in normalize_output(result.output)


def test_ast_all_flags_combined_in_any_order(source_file: Path) -> None:
    result = runner.invoke(
        app, ["ast", str(source_file), "--start", "eval_input", "-c"]
    )

    assert result.exit_code == 0
    assert "compact=True" in normalize_output(result.output)
