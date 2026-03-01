"""Tests for Challenge 094: Reconstruct Corrupted File."""

import hashlib
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from reconstructor import reconstruct


def _make_chunk(directory, number, content, corrupt=False):
    """Create a chunk file with correct or corrupted checksum."""
    checksum = hashlib.md5(content.encode()).hexdigest()
    if corrupt:
        checksum = "0" * 32
    filename = f"chunk_{number:03d}.dat"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as f:
        f.write(f"CHUNK {number} CHECKSUM {checksum}\n")
        f.write(content)
    return filepath


def test_single_chunk():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 1, "Hello, World!")
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["status"] == "ok"
        assert result["chunks_processed"] == 1
        assert result["chunks_repaired"] == 0
        with open(output) as f:
            assert "Hello, World!" in f.read()


def test_multiple_chunks_in_order():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 1, "Part one.")
        _make_chunk(chunks_dir, 2, "Part two.")
        _make_chunk(chunks_dir, 3, "Part three.")
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["chunks_processed"] == 3
        with open(output) as f:
            content = f.read()
        assert content.index("Part one.") < content.index("Part two.")
        assert content.index("Part two.") < content.index("Part three.")


def test_chunks_out_of_order():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 3, "Third.")
        _make_chunk(chunks_dir, 1, "First.")
        _make_chunk(chunks_dir, 2, "Second.")
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        with open(output) as f:
            content = f.read()
        assert content.index("First.") < content.index("Second.")
        assert content.index("Second.") < content.index("Third.")


def test_corrupted_checksum_detected():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 1, "Good content.", corrupt=False)
        _make_chunk(chunks_dir, 2, "Also good.", corrupt=True)
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["chunks_repaired"] == 1
        assert result["chunks_processed"] == 2


def test_multiple_corrupted_chunks():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 1, "Content A.", corrupt=True)
        _make_chunk(chunks_dir, 2, "Content B.", corrupt=True)
        _make_chunk(chunks_dir, 3, "Content C.", corrupt=False)
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["chunks_repaired"] == 2
        assert result["chunks_processed"] == 3


def test_output_file_created():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        _make_chunk(chunks_dir, 1, "Data.")
        output = os.path.join(out_dir, "result.txt")
        reconstruct(chunks_dir, output)
        assert os.path.isfile(output)


def test_multiline_chunk_content():
    with tempfile.TemporaryDirectory() as chunks_dir, tempfile.TemporaryDirectory() as out_dir:
        content = "Line one.\nLine two.\nLine three."
        _make_chunk(chunks_dir, 1, content)
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["chunks_repaired"] == 0
        with open(output) as f:
            text = f.read()
        assert "Line one." in text
        assert "Line two." in text
        assert "Line three." in text


def test_setup_chunks_can_be_processed():
    chunks_dir = str(Path(__file__).parent.parent / "setup" / "chunks")
    with tempfile.TemporaryDirectory() as out_dir:
        output = os.path.join(out_dir, "output.txt")
        result = reconstruct(chunks_dir, output)
        assert result["status"] == "ok"
        assert result["chunks_processed"] == 7
        assert result["chunks_repaired"] >= 1
        assert os.path.isfile(output)
        with open(output) as f:
            content = f.read()
        assert len(content) > 0
