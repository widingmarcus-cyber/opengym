"""Tests for Challenge 073: Fix Path Traversal."""

import sys
import os
import tempfile
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from file_server import serve_file


@pytest.fixture
def file_tree(tmp_path):
    (tmp_path / "public").mkdir()
    (tmp_path / "public" / "index.html").write_text("<h1>Hello</h1>")
    (tmp_path / "public" / "about.txt").write_text("About page")
    (tmp_path / "public" / "subdir").mkdir()
    (tmp_path / "public" / "subdir" / "page.txt").write_text("Sub page")
    (tmp_path / "secret.txt").write_text("TOP SECRET")
    return tmp_path


def test_serve_valid_file(file_tree):
    result = serve_file(str(file_tree / "public"), "index.html")
    assert result == "<h1>Hello</h1>"


def test_serve_file_in_subdirectory(file_tree):
    result = serve_file(str(file_tree / "public"), "subdir/page.txt")
    assert result == "Sub page"


def test_serve_another_valid_file(file_tree):
    result = serve_file(str(file_tree / "public"), "about.txt")
    assert result == "About page"


def test_reject_basic_traversal(file_tree):
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "../secret.txt")


def test_reject_deep_traversal(file_tree):
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "../../../etc/passwd")


def test_reject_url_encoded_traversal(file_tree):
    from urllib.parse import unquote
    encoded_path = "%2e%2e%2fsecret.txt"
    with pytest.raises((PermissionError, FileNotFoundError)):
        serve_file(str(file_tree / "public"), encoded_path)


def test_reject_double_encoded_traversal(file_tree):
    encoded_path = "..%2fsecret.txt"
    with pytest.raises((PermissionError, FileNotFoundError)):
        serve_file(str(file_tree / "public"), encoded_path)


def test_file_not_found(file_tree):
    with pytest.raises(FileNotFoundError):
        serve_file(str(file_tree / "public"), "nonexistent.txt")


# --- Tests that require PermissionError specifically (not FileNotFoundError) ---

def test_basic_traversal_raises_permission_error(file_tree):
    """Basic ../secret.txt must raise PermissionError, not FileNotFoundError."""
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "../secret.txt")


def test_reject_absolute_path_unix(file_tree):
    """Absolute Unix paths like /etc/passwd must raise PermissionError."""
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "/etc/passwd")


def test_reject_absolute_path_windows(file_tree):
    """Absolute Windows paths must raise PermissionError."""
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "C:\\Windows\\system.ini")


def test_reject_mixed_separator_traversal(file_tree):
    """Mixed separators like ..\\/ must raise PermissionError."""
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "..\\/secret.txt")


def test_reject_backslash_traversal(file_tree):
    """Backslash traversal ..\\secret.txt must raise PermissionError."""
    with pytest.raises(PermissionError):
        serve_file(str(file_tree / "public"), "..\\secret.txt")
