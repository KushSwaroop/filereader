import tempfile
import os
import pytest
from io import StringIO
from contextlib import redirect_stdout
from termcolor import colored
from filereaderfinalproject import FancyFileReader  # Adjust path if needed


@pytest.fixture
def sample_file():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as f:
        f.write("This is a test line.\nAnother line with Python.\nEnd of file.")
        temp_name = f.name
    yield temp_name
    os.unlink(temp_name)


@pytest.mark.parametrize(
    "query, color, expected_found",
    [
        ("Python", "blue", True),
        ("Java", "green", False),
        ("line", "magenta", True),
    ],
)
def test_search_string(sample_file, query, color, expected_found):
    reader = FancyFileReader(sample_file)

    with StringIO() as buf, redirect_stdout(buf):
        reader.search_string(query, color)
        output = buf.getvalue()

    if expected_found:
        # Use ANSI-colored version of query
        colored_query = colored(query, color, attrs=["bold"])
        assert colored_query in output
        assert "Line" in output
    else:
        assert "No matches found." in output
