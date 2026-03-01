"""Tests for Challenge 093: Implement File Rotation."""

import os
import re
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from rotator import FileRotator


def test_write_creates_file():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path)
        rotator.write("hello\n")
        assert os.path.isfile(log_path)
        with open(log_path) as f:
            assert f.read() == "hello\n"


def test_write_appends():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path)
        rotator.write("line1\n")
        rotator.write("line2\n")
        with open(log_path) as f:
            assert f.read() == "line1\nline2\n"


def test_manual_rotate():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path)
        rotator.write("some content\n")
        rotator.rotate()
        archived = rotator.get_archived_files()
        assert len(archived) == 1
        assert re.search(r"app\.log\.\d{4}-\d{2}-\d{2}-\d{6}$", archived[0])
        assert not os.path.isfile(log_path) or os.path.getsize(log_path) == 0


def test_auto_rotate_on_size():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path, max_size_bytes=50)
        rotator.write("a" * 30 + "\n")
        rotator.write("b" * 30 + "\n")
        archived = rotator.get_archived_files()
        assert len(archived) >= 1
        with open(log_path) as f:
            content = f.read()
        assert "b" * 30 in content


def test_rotate_empty_file_does_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path)
        rotator.rotate()
        assert len(rotator.get_archived_files()) == 0


def test_cleanup_removes_oldest():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path, max_files=2, max_size_bytes=20)
        for i in range(5):
            rotator.write(f"entry {i}\n")
            time.sleep(0.01)
            if os.path.isfile(log_path) and os.path.getsize(log_path) > 0:
                rotator.rotate()
        rotator.cleanup()
        archived = rotator.get_archived_files()
        assert len(archived) <= 2


def test_get_archived_files_sorted():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path, max_size_bytes=10)
        rotator.write("aaaa\n")
        time.sleep(1.1)
        rotator.rotate()
        rotator.write("bbbb\n")
        time.sleep(1.1)
        rotator.rotate()
        archived = rotator.get_archived_files()
        assert len(archived) == 2
        assert archived[0] < archived[1]


def test_archived_file_contains_original_content():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "app.log")
        rotator = FileRotator(log_path)
        rotator.write("important log data\n")
        rotator.rotate()
        archived = rotator.get_archived_files()
        with open(archived[0]) as f:
            assert f.read() == "important log data\n"
