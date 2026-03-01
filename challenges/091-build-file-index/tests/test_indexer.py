"""Tests for Challenge 091: Build File Index."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from indexer import index_directory


def _build_tree(base):
    """Build a small file tree for testing."""
    os.makedirs(os.path.join(base, "sub1"), exist_ok=True)
    os.makedirs(os.path.join(base, "sub2"), exist_ok=True)

    files = {
        "a.txt": "hello world",
        "b.txt": "hello world",
        "sub1/c.py": "print('hi')",
        "sub1/d.py": "x = 1\ny = 2\nz = 3\n",
        "sub2/e.csv": "a,b\n1,2\n3,4\n5,6\n",
        "sub2/f.csv": "x,y\n10,20\n",
        "sub2/g.json": '{"key": "value"}',
        "noext": "file without extension",
    }
    for relpath, content in files.items():
        full = os.path.join(base, relpath)
        with open(full, "w") as fh:
            fh.write(content)
    return files


def test_total_files():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        assert result["total_files"] == 8


def test_total_size():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        assert result["total_size"] > 0
        expected = sum(
            len(c.encode()) for c in [
                "hello world", "hello world", "print('hi')",
                "x = 1\ny = 2\nz = 3\n", "a,b\n1,2\n3,4\n5,6\n",
                "x,y\n10,20\n", '{"key": "value"}', "file without extension",
            ]
        )
        assert result["total_size"] == expected


def test_file_types():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        ft = result["file_types"]
        assert ft[".txt"] == 2
        assert ft[".py"] == 2
        assert ft[".csv"] == 2
        assert ft[".json"] == 1
        assert ft[""] == 1


def test_largest_files_order():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        largest = result["largest_files"]
        sizes = [s for _, s in largest]
        assert sizes == sorted(sizes, reverse=True)


def test_largest_files_limit():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        assert len(result["largest_files"]) <= 5


def test_duplicate_groups_detected():
    with tempfile.TemporaryDirectory() as tmp:
        _build_tree(tmp)
        result = index_directory(tmp)
        dups = result["duplicate_groups"]
        dup_flat = [p for group in dups for p in group]
        assert any("a.txt" in p for p in dup_flat)
        assert any("b.txt" in p for p in dup_flat)


def test_no_false_duplicates():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "d"))
        with open(os.path.join(tmp, "d", "unique1.txt"), "w") as f:
            f.write("content alpha")
        with open(os.path.join(tmp, "d", "unique2.txt"), "w") as f:
            f.write("content beta")
        result = index_directory(tmp)
        assert len(result["duplicate_groups"]) == 0


def test_sample_tree():
    sample = str(Path(__file__).parent.parent / "setup" / "sample_tree")
    result = index_directory(sample)
    assert result["total_files"] == 20
    assert result["total_size"] > 0
    assert ".py" in result["file_types"]
    assert ".csv" in result["file_types"]
    assert len(result["duplicate_groups"]) >= 1
