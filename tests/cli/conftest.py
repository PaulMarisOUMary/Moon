import pytest
import re

from pathlib import Path


@pytest.fixture()
def source_file(tmp_path: Path) -> Path:
    path = tmp_path / "main.mn"
    path.write_text("print 1\n")
    return path


def normalize_output(output: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)

    normalized = re.sub(r'[\s\u2500-\u257F]+', ' ', output)
    
    return normalized.strip()